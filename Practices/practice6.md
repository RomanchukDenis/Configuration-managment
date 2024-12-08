# Практическое задание №6. Системы автоматизации сборки

Работа с утилитой Make.

## Задача 1

Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше.

```
import re

with open("civgraph.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)
    
    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
    
    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```

<img width="1439" alt="image" src="https://github.com/user-attachments/assets/1c0fd2ba-e4b5-4cdb-9e71-00d841ffc75e">

## Задача 2

Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".

> Добавляется строка makefile.write(f"\t@touch {target}\n") для создания или обновления целевого файла с временной меткой

```
import re

with open("civgraph.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)

    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
        makefile.write(f"\t@touch {target}\n")

    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```

<img width="1473" alt="image" src="https://github.com/user-attachments/assets/340c9670-9cf9-4328-8247-e7d1a69e4b1e">

## Задача 3
Добавить цель clean, не забыв и про "животное".

## Задача 4
Написать makefile для следующего скрипта сборки:

```
gcc prog.c data.c -o prog
dir /B > files.lst
7z a distr.zip *.*
```

Вместо gcc можно использовать другой компилятор командной строки, но на вход ему должны подаваться два модуля: prog и data. Если используете не Windows, то исправьте вызовы команд на их эквиваленты из вашей ОС. В makefile должны быть, как минимум, следующие задачи: all, clean, archive. Обязательно покажите на примере, что уже сделанные подзадачи у вас не перестраиваются.
