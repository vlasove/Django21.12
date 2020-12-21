## Предварительная подготовка

Проходим предварительную подготовку в 2 этапа

### Этап 1. Разминка.
Для прохождения разминки (ограничение по времени в ней нет) нужно перейти по ссылке:
https://contest.yandex.ru/contest/23816

* Решим задачу A:
```
"""
Train:A solution
"""

name = input()
lastname = input()
age = input()

answer = f"Имя: {name} , Фамилия: {lastname} , Возраст: {age} . Студент BPS"
print(answer)
```
***Важно*** не использовать прилглашения на ввод ```input("Please enter value:")```, внимательно следить за пунктуацией, пробелами и семантикой ответов.


* Решим задачу B:
```
"""
Train B: solution
"""
a_side = int(input())
b_side = int(input())

perimeter = 2 * (a_side + b_side)
area = a_side * b_side

print(f"Периметр: {perimeter}")
print(f"Площадь: {area}")
```