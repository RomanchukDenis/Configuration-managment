# Практическое работа  №1
## Задача 1: Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd

### Код
```
grep '^[^:]*' /etc/passwd | cut -d: -f1 | sort
```
### Вывод
<img width="603" alt="image" src="https://github.com/user-attachments/assets/e0a448f5-3d0e-4e3b-8459-26bb7a1cc812">

## Задача 2: Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов

### Код
```
cat /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```
### Вывод
<img width="602" alt="image" src="https://github.com/user-attachments/assets/211530f6-a700-49d2-a944-bff871a32996">

## Задача 3: Написать программу banner средствами bash для вывода текстов 

### Код
```
#!/bin/bash

text="Hello from RTU MIREA!"
length=${#text}

for i in $(seq 1 $((length + 2))); do
    line+="-"
done

echo "+${line}+"
echo "| ${text} |"
echo "+${line}+"
```

### Вывод
<img width="604" alt="image" src="https://github.com/user-attachments/assets/8e295225-33e7-45ad-b888-95569cbae1dc">

## Задача 4: Написать программу для вывода всех идентификаторов 

### Код
```
#!/bin/bash

file="$1"

id=$(grep -o -E '\b[a-zA-Z]*\b' "$file" | sort -u)
```
```
grep -oE '\b[a-zA-Z_][a-zA-Z0-9_]*\b' hello.c | grep -vE '\b(int|void|return|if|else|for|while|include|stdio)\b' | sort | uniq
```
### Вывод
<img width="1123" alt="image" src="https://github.com/user-attachments/assets/624be27c-fae5-4194-91cb-bda889a4c2a7">

## Задача 5: Написать программу для реализации пользовательской команды

### Код
```
#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Используйте: $0 имя команды."
	exit 1
fi

command_name="$1"
command_path="./$command_name"

if [ ! -f "$command_path" ]; then
	echo "Ошибка: файл '$command_path' не найден."
	exit 1
fi

sudo chmod +x "$command_name"
sudo cp "$command_path" /usr/local/bin/

if [ $? -ne 0 ]; then
	echo "Ошибка: не удалось скопировать файл."
	exit 1
fi

sudo chmod 775 /usr/local/bin/"$command_name"

if [ $? -ne 0 ]; then
	echo "Ошибка: не удалось установить права для '$command_name'."
	exit 1
fi

echo "Команда '$command_name' успешно зарегестрирована."
```

### Вывод
<img width="810" alt="image" src="https://github.com/user-attachments/assets/d16cc840-c9c8-4973-ab82-5f6d5a4dce24">

## Задача 6: Написать программу для проверки наличия комментария в первой строке файлов с расширением c,js и py

### Код
```
# -*- coding: utf-8 -*-
import os
import sys

def check_comment_in_first_line(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        if first_line.startswith('#') or first_line.startswith('//') or first_line.startswith('/*'):
            return True
    return False

def check_files_in_directory(directory):
    extensions = ('.c', '.js', '.py')
    for filename in os.listdir(directory):
        if filename.endswith(extensions):
            file_path = os.path.join(directory, filename)
            if check_comment_in_first_line(file_path):
                print(f"Комментарий найден в файле: {filename}")
            else:
                print(f"Комментарий не найден в файле: {filename}")

if name == 'main':
    if len(sys.argv) != 2:
        print("Использование: python3 main.py ~/Desktop/питон")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"{directory} не является директорией.")
        sys.exit(1)

    check_files_in_directory(directory)
```
#### Вывод
<img width="567" alt="image" src="https://github.com/user-attachments/assets/7997d312-6473-483a-bb99-56d9c76b2415">

## Задача 7: Написать программу для нахождения файлов-дубликатов 

### Код
```
#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "Использование: $0 /путь/к/каталогу."
	exit 1
fi

directory=$1

if [[ ! -d $directory ]]; then
	echo "Ошибка: каталог $directory не найден."
	exit 1
fi

declare -A file_hashes

while IFS= read -r -d '' file; do
	hash=$(sha256sum "$file" | awk '{ print $1 }')
	file_hashes["$hash"]+="file"$'\n'
done < <(find "$directory" -type f -print0)

found_duplicates=false

for hash in "${!file_hashes[@]}"; do
	files="${file_hashes[$hash]}"
	files_count=$(echo -e "files" | wc -l)


	if [[ $files_count -gt 1 ]]; then
		found_duplicates=true
		echo "Найдены дубликаты:"
		echo -e "$files"
	fi
done

if ! $found_duplicates; then
	echo "Дубликатов не найдено."
	exit 1
fi
```
#### Вывод
<img width="794" alt="image" src="https://github.com/user-attachments/assets/a30e2c3f-6556-4ec0-aa9b-e007d1aeb6fb">

## Задача 8: Написать программу, которая находит все файлы в данном каталоге с расширеннием, указанным в качестве аргумента и архивирует все эти файлы в архив tar

### Код
```
import os
import tarfile
import sys


def archive(directory, extension):
    tar_filename = f"archive_{extension.replace('.', '')}.tar"

    with tarfile.open(tar_filename, "w") as tar:
        for file in os.listdir(directory):
            if file.endswith(extension):
                tar.add(os.path.join(directory, file))
    print(f"Архив {tar_filename} создан.")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[2][0] != ".":
        print("Usage: ./archive.py <directory> <extension> (with .)")
    else:
        directory, extension = sys.argv[1], sys.argv[2]
        archive(directory, extension)
```
#### Вывод
<img width="985" alt="image" src="https://github.com/user-attachments/assets/024c72ab-5dc2-4bdc-a244-31c5f7e6d8d9">

## Задача 9: Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файл задаются аргументами

### Код
```
#!/bin/bash

if [ "$#" -ne 2 ]; then
	echo "Использование: $0 <входной_файл> <выходной_файл>"
	exit 1
fi

input_file="$1"
output_file="$2"

if [ ! -f "$input_file" ]; then
	echo "Ошибка: '$input_file' не найден."
	exit 1
fi

sed 's/    /\t/g' "$input_file" > "$output_file"

echo "Заменено в файле: '$output_file'"
```
#### Вывод
<img width="1008" alt="image" src="https://github.com/user-attachments/assets/29f914f7-32e6-47ca-81d7-40a34ae708d4">

## Задача 10: Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории

### Код
```
#!/bin/bash

if [ "$#" -ne 1 ]; then
	echo "Использование: $0 /путь/к/каталогу."
	exit 1
fi

directory="$1"

if [ ! -d "$directory" ]; then
	echo: "Ошибка: указанный каталог '$directory' не существует."
	exit 1
fi

find "$directory" -type f -name "*.txt" -empty -exec basename {} \;
```
#### Вывод
<img width="683" alt="image" src="https://github.com/user-attachments/assets/af28d762-22ce-4157-839e-17778f033e25">
