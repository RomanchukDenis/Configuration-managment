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

