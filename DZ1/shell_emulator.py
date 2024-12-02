import os
import tarfile
import json
import sys
import re
import shutil
from pathlib import Path

def log_action(log_file, user, action):
    with open(log_file, 'a') as log:
        log.write(json.dumps({"user": user, "action": action}) + "\n")


def is_valid_directory_path(path):
    invalid_patterns = [
        r"\.\./",  # Папка с '..' в пути
        r"//",  # Множественные слэши
        r"\.\.+",  # Много точек подряд
        r"\.\./",  # Попытка подняться на уровень выше
        r"[^\w./-]"  # Любые нежелательные символы
    ]

    for pattern in invalid_patterns:
        if re.search(pattern, path):
            return False
    return True

def cleanup(temp_mount_path):
    # Очистка временной директории
    if temp_mount_path.exists():
        print("Удаляем временную директорию temp_mount...")
        shutil.rmtree(temp_mount_path)
    else:
        print("Ошибка: Директория temp_mount не существует.")

def main(username, hostname, vfs_path, log_file, script_path=None):
    # Проверка существования архива
    if not os.path.exists(vfs_path):
        print(f"Ошибка: файл {vfs_path} не найден.")
        sys.exit(1)

    # Проверка и очистка директории temp_mount
    temp_mount_path = Path("temp_mount")

    if temp_mount_path.exists():
        if temp_mount_path.is_dir():
            print("Удаляем старое содержимое temp_mount...")
            shutil.rmtree(temp_mount_path)
        else:
            print(f"Ошибка: {temp_mount_path} существует, но это не директория.")
            sys.exit(1)

    # Создаем директорию temp_mount
    print("Создаем директорию temp_mount...")
    os.makedirs(temp_mount_path)

    # Распаковка виртуальной файловой системы
    print(f"Распаковываем архив {vfs_path} в {temp_mount_path}...")
    with tarfile.open(vfs_path, "r") as tar:
        tar.extractall(temp_mount_path)

    # Устанавливаем директорию temp_vfs как корневую
    current_dir = temp_mount_path / "temp_vfs"
    if not current_dir.exists():
        print("Ошибка: Директория temp_vfs не найдена после распаковки.")
        sys.exit(1)

    print(f"Текущая рабочая директория после распаковки: {current_dir}")
    log_action(log_file, username, "Эмулятор запущен.")

    # Выполнение стартового скрипта, если указан
    # Выполнение стартового скрипта, если указан
    if script_path:
        try:
            # Сохраняем текущую директорию
            original_dir = os.getcwd()

            # Определяем полный путь к стартовому скрипту
            script_full_path = Path(original_dir) / script_path

            # Проверяем, существует ли скрипт
            if not script_full_path.exists():
                raise FileNotFoundError(f"Файл {script_path} не найден.")

            # Переходим в temp_mount перед выполнением скрипта
            os.chdir(current_dir)

            with open(script_full_path) as script:
                commands = script.readlines()

            for cmd in commands:
                print(f"$ {cmd.strip()}")
                os.system(cmd.strip())

            # Возвращаемся в исходную директорию
            os.chdir(original_dir)

        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при выполнении скрипта: {e}")
            os.chdir(original_dir)  # Возвращаемся в исходную директорию при ошибке
            sys.exit(1)

    while True:
        # Вывод приглашения
        cmd = input(f"{username}@{hostname}:{current_dir} $ ").strip()

        if cmd.startswith("cd "):
            new_dir = cmd.split(" ", 1)[1]
            if new_dir == "..":
                if current_dir == temp_mount_path / "temp_vfs":
                    print(f"Ошибка: Уже находитесь в корневой директории {current_dir}.")
                else:
                    parent_dir = current_dir.parent
                    current_dir = parent_dir
                    log_action(log_file, username, f"cd ..")
            elif new_dir == "/":
                current_dir = temp_mount_path / "temp_vfs"
                log_action(log_file, username, f"cd /")
            elif not is_valid_directory_path(new_dir):
                print(f"Ошибка: Некорректный путь '{new_dir}'.")
                continue
            else:
                new_path = current_dir / new_dir
                if new_path.is_dir():
                    current_dir = new_path
                    log_action(log_file, username, f"cd {new_dir}")
                else:
                    print(f"Ошибка: Директория {new_dir} не найдена.")
        elif cmd == "ls":
            os.system(f"ls {current_dir}")
            log_action(log_file, username, "ls")
        elif cmd == "exit":
            log_action(log_file, username, "Эмулятор завершен.")
            print("Выход из эмулятора.")
            break
        elif cmd == "who":
            print(f"Текущий пользователь: {username}")
            log_action(log_file, username, "who")
        elif cmd.startswith("rm "):
            filename = cmd.split(" ", 1)[1]
            file_path = current_dir / filename
            if not is_valid_directory_path(filename):
                print(f"Ошибка: Некорректный путь '{filename}'.")
                continue
            if file_path.exists() and file_path.is_file():
                os.remove(file_path)
                print(f"Файл {filename} удален.")
                log_action(log_file, username, f"rm {filename}")
            else:
                print(f"Ошибка: Файл {filename} не найден.")
        elif cmd.startswith("head "):
            filename = cmd.split(" ", 1)[1]
            file_path = current_dir / filename
            if not is_valid_directory_path(filename):
                print(f"Ошибка: Некорректный путь '{filename}'.")
                continue
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'r') as f:
                    for _ in range(10):  # Показываем первые 10 строк
                        print(f.readline().strip())
                log_action(log_file, username, f"head {filename}")
            else:
                print(f"Ошибка: Файл {filename} не найден.")
        else:
            print(f"Команда '{cmd}' не распознана.")

    # Очистка временной директории по завершению работы
    cleanup(temp_mount_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Эмулятор UNIX shell.")
    parser.add_argument("--user", required=True, help="Имя пользователя.")
    parser.add_argument("--host", required=True, help="Имя компьютера.")
    parser.add_argument("--vfs", required=True, help="Путь к архиву виртуальной файловой системы.")
    parser.add_argument("--log", required=True, help="Путь к лог-файлу.")
    parser.add_argument("--script", help="Путь к стартовому скрипту.", default=None)

    args = parser.parse_args()
    main(args.user, args.host, args.vfs, args.log, args.script)


"""import os
import tarfile
import json
import sys
import re
import shutil
from pathlib import Path


def log_action(log_file, user, action):
    with open(log_file, 'a') as log:
        log.write(json.dumps({"user": user, "action": action}) + "\n")


def is_valid_directory_path(path):
    #Проверка корректности пути. Не допускаются '..' и слишком много слэшей.
    invalid_patterns = [
        r"\.\./",  # Папка с '..' в пути
        r"//",  # Множественные слэши
        r"\.\.+",  # Много точек подряд
        r"\.\./",  # Попытка подняться на уровень выше
        r"[^\w./-]"  # Любые нежелательные символы
    ]

    for pattern in invalid_patterns:
        if re.search(pattern, path):
            return False
    return True


def main(username, hostname, vfs_path, log_file, script_path=None):
    # Проверка существования архива
    if not os.path.exists(vfs_path):
        print(f"Ошибка: файл {vfs_path} не найден.")
        sys.exit(1)

    # Проверка и очистка директории temp_mount
    temp_mount_path = Path("temp_mount")

    if temp_mount_path.exists():
        if temp_mount_path.is_dir():
            # Удаляем старое содержимое
            print("Удаляем старое содержимое temp_mount...")
            shutil.rmtree(temp_mount_path)
        else:
            print(f"Ошибка: {temp_mount_path} существует, но это не директория.")
            sys.exit(1)

    # Создаем директорию temp_mount
    print("Создаем директорию temp_mount...")
    os.makedirs(temp_mount_path)

    # Распаковка виртуальной файловой системы
    print(f"Распаковываем архив {vfs_path} в {temp_mount_path}...")
    with tarfile.open(vfs_path, "r") as tar:
        tar.extractall(temp_mount_path)


    # Устанавливаем директорию temp_vfs как корневую
    current_dir = temp_mount_path / "temp_vfs"  # Убедитесь, что эта директория существует
    if not current_dir.exists():
        print("Ошибка: Директория temp_vfs не найдена после распаковки.")
        sys.exit(1)

    print(f"Текущая рабочая директория после распаковки: {current_dir}")

    log_action(log_file, username, "Эмулятор запущен.")

    # Выполнение стартового скрипта, если указан
    if script_path:
        with open(script_path) as script:
            commands = script.readlines()
        for cmd in commands:
            print(f"$ {cmd.strip()}")
            os.system(cmd.strip())

    while True:
        # Вывод приглашения
        cmd = input(f"{username}@{hostname}:{current_dir} $ ").strip()

        if cmd.startswith("cd "):
            new_dir = cmd.split(" ", 1)[1]
            if new_dir == "..":
                # Переход в родительскую директорию
                if current_dir == temp_mount_path / "temp_vfs":  # Мы находимся в корневой директории
                    print(f"Ошибка: Уже находитесь в корневой директории {current_dir}.")
                else:
                    parent_dir = current_dir.parent
                    current_dir = parent_dir
                    log_action(log_file, username, f"cd ..")
            elif new_dir == "/":
                # Переход в корневую директорию
                current_dir = temp_mount_path / "temp_vfs"
                log_action(log_file, username, f"cd /")
            elif not is_valid_directory_path(new_dir):
                print(f"Ошибка: Некорректный путь '{new_dir}'.")
                continue
            else:
                new_path = current_dir / new_dir
                if new_path.is_dir():
                    current_dir = new_path
                    log_action(log_file, username, f"cd {new_dir}")
                else:
                    print(f"Ошибка: Директория {new_dir} не найдена.")
        elif cmd == "ls":
            os.system(f"ls {current_dir}")
            log_action(log_file, username, "ls")
        elif cmd == "exit":
            log_action(log_file, username, "Эмулятор завершен.")
            print("Выход из эмулятора.")
            break
        elif cmd == "who":
            print(f"Текущий пользователь: {username}")
            log_action(log_file, username, "who")
        elif cmd.startswith("rm "):
            filename = cmd.split(" ", 1)[1]
            file_path = current_dir / filename
            if not is_valid_directory_path(filename):
                print(f"Ошибка: Некорректный путь '{filename}'.")
                continue
            if file_path.exists() and file_path.is_file():
                os.remove(file_path)
                print(f"Файл {filename} удален.")
                log_action(log_file, username, f"rm {filename}")
            else:
                print(f"Ошибка: Файл {filename} не найден.")
        elif cmd.startswith("head "):
            filename = cmd.split(" ", 1)[1]
            file_path = current_dir / filename
            if not is_valid_directory_path(filename):
                print(f"Ошибка: Некорректный путь '{filename}'.")
                continue
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'r') as f:
                    for _ in range(10):  # Показываем первые 10 строк
                        print(f.readline().strip())
                log_action(log_file, username, f"head {filename}")
            else:
                print(f"Ошибка: Файл {filename} не найден.")
        else:
            print(f"Команда '{cmd}' не распознана.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Эмулятор UNIX shell.")
    parser.add_argument("--user", required=True, help="Имя пользователя.")
    parser.add_argument("--host", required=True, help="Имя компьютера.")
    parser.add_argument("--vfs", required=True, help="Путь к архиву виртуальной файловой системы.")
    parser.add_argument("--log", required=True, help="Путь к лог-файлу.")
    parser.add_argument("--script", help="Путь к стартовому скрипту.", default=None)

    args = parser.parse_args()
    main(args.user, args.host, args.vfs, args.log, args.script)"""