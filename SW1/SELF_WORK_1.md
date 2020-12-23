## Самостоятельная работа 1

***Техническое задание*** : реализовать функционал ```login```, ```logout``` , ```signup``` для пользовательской модели ```CustomUser```.

***Описание модели*** : модель ```CustomUser``` представлена в виде:
```
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.TextField(null=True, blank=True) # номер телефона пользователя
    age = models.PositiveIntegerField(null=True, blank=True) # возраст пользователя
    salary_amount = models.FloatField(null=True, blank=True) # зарплата пользователя
```

***Описание в панели администратора***: в панели администратора информация про пользователя должна выводиться в виде: ```username```, ```email```, ```salary_amount```, ```age```, ```phone_number```.

***Набор шаблонов***: cтандартный набор шаблонов:
```
templates/registration/login.html
templates/base.html
templates/home.html
templates/signup.html
```

***Решение*** прислать в чат преподавателю, в виде ссылки на ```github``` репозиторий c исходным кодом проекта.