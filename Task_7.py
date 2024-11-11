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