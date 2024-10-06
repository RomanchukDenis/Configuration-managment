# Практическое работа  №1
## Задача 1: Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd

### Код
```
grep '^[^:]*' /etc/passwd | cut -d: -f1 | sort
```
### Вывод
<img width="603" alt="image" src="https://github.com/user-attachments/assets/e0a448f5-3d0e-4e3b-8459-26bb7a1cc812">
