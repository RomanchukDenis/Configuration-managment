Задание №1
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме CLI.

Ключами командной строки задаются:

• Имя пользователя для показа в приглашении к вводу.

• Имя компьютера для показа в приглашении к вводу.

• Путь к архиву виртуальной файловой системы.

• Путь к лог-файлу.

• Путь к стартовому скрипту.

Лог-файл имеет формат json и содержит все действия во время последнего
сеанса работы с эмулятором. Для каждого действия указан пользователь.
Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.

Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:

1. head.

2. rm.

3. who.

Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.
_____________________________________________________________________________________________________________________________
## 1. Запуск программы
```
python3 shell_emulator.py --user denis --host virtualmachine --vfs virtual_fs.tar --log session_log.json --script startup_script.sh
```
_____________________________________________________________________________________________________________________________
## 2. Структура проекта
shell_emulator.py        # Основной файл эмулятора

virtual_fs.tar           # Архив виртуальной файловой системы

session_log.json         # Лог-файл сеанса работы

startup_script.sh        # Стартовый скрипт

test_shell_emulator.py   # Тесты для эмулятора

_____________________________________________________________________________________________________________________________
## 3. Тест работоспособности

##Запуск тестирования 

```
python3 -m unittest test_shell.py

```
Результат

<img width="571" alt="image" src="https://github.com/user-attachments/assets/d56c0da9-6428-4012-8a17-0ef0dfcd65ef">




