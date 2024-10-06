# Практическая работа №2
## Задача 1: Вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

### Код
```
 pip show matplotlib
```
### Вывод
<img width="798" alt="image" src="https://github.com/user-attachments/assets/06081871-5659-448b-a0bf-a763956e288e">

## Задача 2: Вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

### Код
```
npm show express
```
### Вывод
<img width="1171" alt="image" src="https://github.com/user-attachments/assets/75d9d24a-bdd6-41da-b365-4ec8dd1f7dfb">

## Задача 3: Сформировать graphviz-код и получить изображения зависимостей matplotlib и express.

### Код для matplotlib
```
digraph MatplotlibDependencies {
    "matplotlib" -> "numpy";
    "matplotlib" -> "pillow";
    "matplotlib" -> "cycler";
    "matplotlib" -> "kiwisolver";
    "matplotlib" -> "pyparsing";
    "matplotlib" -> "python-dateutil";
}
```
```
dot -Tpng matplotlib.dot -o matplotlib_dependencies.png
```
### Код для express
```
digraph ExpressDependencies {
    "express" -> "accepts";
    "express" -> "array-flatten";
    "express" -> "body-parser";
    "express" -> "content-disposition";
    "express" -> "content-type";
    "express" -> "cookie";
    "express" -> "cookie-signature";
    "express" -> "debug";
    "express" -> "depd";
    "express" -> "encodeurl";
    "express" -> "escape-html";
    "express" -> "etag";
}
```
```
dot -Tpng express.dot -o express_dependencies.png
```
### Вывод matplotlib
![image](https://github.com/user-attachments/assets/d60b7e14-43c3-4cf5-a255-1d8e50210192)
### Вывод express
![image](https://github.com/user-attachments/assets/468eeff9-bb80-4d4d-a803-81c5ad7ab865)


## Задача 4: Решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (подсказка: используйте all_different). Найти минимальное решение для суммы 3 цифр.

### Код
```
include "globals.mzn";

int: N = 6; % Количество цифр в билете
array[1..N] of var 0..9: digits; % Массив для хранения цифр билета

constraint all_different(digits);

constraint sum(digits[1..3]) = sum(digits[4..6]);

constraint digits[1] > 0;

solve minimize sum(digits[1..3]);

output ["Digits: \(digits)\n"];
```
### Вывод
<img width="555" alt="image" src="https://github.com/user-attachments/assets/422987bd-5ca4-4fb7-b114-ffb767afe975">

## Задача 5: Решить на MiniZinc задачу о зависимостях пакетов для рисунка, приведенного ниже.
<img width="585" alt="image" src="https://github.com/user-attachments/assets/c9cd0a81-8573-4b38-8a75-ecf8b561626e">

### Код
```
include "globals.mzn";

% Определение версий с уникальными именами
enum VersionsMenu = { menu_v1_0_0, menu_v1_1_0, menu_v1_2_0, menu_v1_3_0, menu_v1_4_0, menu_v1_5_0 };
enum VersionsDropdown = { dropdown_v1_8_0, dropdown_v2_0_0, dropdown_v2_1_0, dropdown_v2_2_0, dropdown_v2_3_0 };
enum VersionsIcons = { icons_v1_0_0, icons_v2_0_0 };

% Переменные для выбранных версий
var VersionsMenu: menu_version;
var VersionsDropdown: dropdown_version;
var VersionsIcons: icons_version;

% Зависимости версий
constraint
    if menu_version = menu_v1_5_0 then dropdown_version in {dropdown_v2_3_0, dropdown_v2_2_0} /\ icons_version = icons_v2_0_0
    elseif menu_version = menu_v1_4_0 then dropdown_version in {dropdown_v2_2_0, dropdown_v2_1_0} /\ icons_version = icons_v2_0_0
    elseif menu_version = menu_v1_3_0 then dropdown_version in {dropdown_v2_1_0, dropdown_v2_0_0} /\ icons_version = icons_v1_0_0
    elseif menu_version = menu_v1_2_0 then dropdown_version in {dropdown_v2_0_0, dropdown_v1_8_0} /\ icons_version = icons_v1_0_0
    elseif menu_version = menu_v1_1_0 then dropdown_version = dropdown_v1_8_0 /\ icons_version = icons_v1_0_0
    else dropdown_version = dropdown_v1_8_0 /\ icons_version = icons_v1_0_0
    endif;

% Минимизация версии root, которая зависит от версии menu
solve minimize menu_version;
```
### Вывод
<img width="302" alt="image" src="https://github.com/user-attachments/assets/1788c0a4-76ec-41d3-99c8-3a41dbfac611">

## Задача 6: Решить на MiniZinc задачу о зависимостях пакетов для следующих данных:
```
root 1.0.0 зависит от foo ^1.0.0 и target ^2.0.0.
foo 1.1.0 зависит от left ^1.0.0 и right ^1.0.0.
foo 1.0.0 не имеет зависимостей.
left 1.0.0 зависит от shared >=1.0.0.
right 1.0.0 зависит от shared <2.0.0.
shared 2.0.0 не имеет зависимостей.
shared 1.0.0 зависит от target ^1.0.0.
target 2.0.0 и 1.0.0 не имеют зависимостей.
```

### Код
```
include "globals.mzn";

int: root = 100;
var 100..300: foo;
var 100..300: target;
var 100..300: left;
var 100..300: right;
var 100..300: shared;

constraint
  root = 100 ->
  (foo >= 100 /\ foo < 200 /\ 
  target >= 200 /\ target < 300);
 
constraint
  foo = 110 -> 
  (left >= 100 /\ left < 200 /\
  right >= 100 /\ right < 200);
 
constraint
  (left = 100 -> shared >= 100) /\
  (right = 100 -> shared < 200);

constraint
  left = 100 ->
  (shared >= 100);
 
constraint
  right = 100 ->
  (shared < 200);
  
constraint
  shared = 100 ->
  (target >= 100 /\ target < 200);

output [
    "Root Version: ", show(root), "\n",
    "Foo Version: ", show(foo), "\n",
    "Left Version: ", show(left), "\n",
    "Right Version: ", show(right), "\n",
    "Shared Version: ", show(shared), "\n",
    "Target Version: ", show(target), "\n"
];
```
### Вывод
<img width="242" alt="image" src="https://github.com/user-attachments/assets/54e881af-30f9-4056-ab1c-db6f5260b644">

## Задача 7: Представить задачу о зависимостях пакетов в общей форме. Здесь необходимо действовать аналогично реальному менеджеру пакетов. То есть получить описание пакета, а также его зависимости в виде структуры данных. Например, в виде словаря. В предыдущих задачах зависимости были явно заданы в системе ограничений. Теперь же систему ограничений надо построить автоматически, по метаданным.

### Код
```
# Структура данных для хранения пакетов и их зависимостей
packages = {
    'root': {
        '1.0.0': {
            'dependencies': {
                'foo': '^1.0.0',
                'target': '^2.0.0'
            }
        }
    },
    'foo': {
        '1.1.0': {
            'dependencies': {
                'left': '^1.0.0',
                'right': '^1.0.0'
            }
        },
        '1.0.0': {
            'dependencies': {}
        }
    },
    'left': {
        '1.0.0': {
            'dependencies': {
                'shared': '>=1.0.0'
            }
        }
    },
    'right': {
        '1.0.0': {
            'dependencies': {
                'shared': '<2.0.0'
            }
        }
    },
    'shared': {
        '2.0.0': {
            'dependencies': {}
        },
        '1.0.0': {
            'dependencies': {
                'target': '^1.0.0'
            }
        }
    },
    'target': {
        '2.0.0': {
            'dependencies': {}
        },
        '1.0.0': {
            'dependencies': {}
        }
    }
}


# Функция проверки совместимости версии пакетов
def check_dependencies(package, version, resolved, packages):
    # Если пакет уже добавлен в решение, пропускаем
    if package in resolved:
        return True

    # Получаем зависимости для указанной версии
    dependencies = packages[package][version]['dependencies']

    for dep_pkg, dep_version in dependencies.items():
        # Проверка совместимости версии зависимостей
        if not resolve_version(dep_pkg, dep_version, packages, resolved):
            return False

    # Добавляем текущий пакет в решенные
    resolved[package] = version
    return True


# Функция выбора совместимой версии
def resolve_version(package, version_range, packages, resolved):
    # Для простоты обрабатываем только некоторые форматы версий
    if version_range.startswith('^'):
        min_version = version_range[1:]  # Минимальная версия для диапазона "^"
        for version in packages[package]:
            if version >= min_version and package not in resolved:
                if check_dependencies(package, version, resolved, packages):
                    return True
    return False


# Основная функция для решения задачи
def solve(packages):
    resolved = {}
    root_version = '1.0.0'  # Задаем корневую версию
    if check_dependencies('root', root_version, resolved, packages):
        print("Решение найдено:", resolved)
    else:
        print("Решение не найдено")


solve(packages)
```
### Вывод
<img width="941" alt="image" src="https://github.com/user-attachments/assets/4e0fd55e-4532-45a0-afc7-7f37780e5d43">
