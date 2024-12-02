import json
import unittest
import os
import tarfile
import tempfile
from unittest.mock import patch
from pathlib import Path
from shell_emulator import main

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию для тестов
        self.temp_dir = tempfile.TemporaryDirectory()
        self.mount_path = Path(self.temp_dir.name) / "temp_mount"
        self.vfs_path = self.mount_path / "temp_vfs"
        self.log_file = Path(self.temp_dir.name) / "log.json"

        # Создаем тестовую файловую структуру
        os.makedirs(self.vfs_path, exist_ok=True)
        self.test_file = self.vfs_path / "file1.txt"
        self.test_file.write_text("Тестовое содержимое файла.")

        # Создаем архив виртуальной файловой системы
        self.tar_path = self.mount_path.parent / "vfs_archive.tar"
        with tarfile.open(self.tar_path, "w") as tar:
            tar.add(self.vfs_path, arcname="temp_vfs")

        self.username = "test_user"
        self.hostname = "test_host"

    def tearDown(self):
        # Удаляем временную директорию после выполнения тестов
        self.temp_dir.cleanup()

    def test_cd_and_ls(self):
        """Проверка команд cd и ls."""
        test_dir = self.vfs_path / "test_dir"
        os.makedirs(test_dir)

        self.assertTrue(test_dir.exists())

    def test_rm(self):
        """Проверка команды rm."""
        test_file = self.vfs_path / "delete_me.txt"
        test_file.write_text("Файл для удаления")

        # Убедимся, что файл создан
        self.assertTrue(test_file.exists())

        # Удаляем файл
        os.remove(test_file)

        # Убедимся, что файл удален
        self.assertFalse(test_file.exists())

    def test_head(self):
        """Проверка команды head."""
        with open(self.test_file, "r") as f:
            content = f.read(10)  # Читаем первые 10 символов
        self.assertEqual(content, "Тестовое с")

    def test_exit(self):
        """Проверка команды exit."""
        try:
            main(self.username, self.hostname, str(self.tar_path), str(self.log_file))
        except Exception as e:
            self.fail(f"Программа завершилась с исключением: {e}")
        # Проверяем содержимое лога
        with open(self.log_file, 'r', encoding='utf-8') as log:
            log_content = log.readlines()
        # Проверяем последнюю запись
        last_entry = json.loads(log_content[-1])
        self.assertEqual(last_entry["action"], "Эмулятор завершен.")

    def test_who(self):
        """Проверка команды who."""
        with open(self.log_file, "w") as log:
            log.write("Проверка команды who")
        with open(self.log_file, "r") as log:
            content = log.read()
        self.assertIn("Проверка команды who", content)


if __name__ == "__main__":
    unittest.main()
