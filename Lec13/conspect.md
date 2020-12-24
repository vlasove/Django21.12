## Лекция 13. Django Blog. P1

***Задача:*** создать полноценный блог , где:
* пользователь умеет ```/login, /logout/, signup/``` - первичный аккаунтинг
* также пользователь умеет ```/password_reset, /password_change````
* можно создавать статьи ```articles/new```
* можно редактировать статьи ```articles/<int:pk>/edit```
* можно удалять статьи ```articles/<int:pk>/delete```
* можно посмотреть детально статью ```articles/<int:pk>/detail```
* можно посмотреть на список всех статей ```articles/```
* еще есть домашняя страница и панель навигации

### Шаг 0. Инициализация проекта
* Копируем все из ```Lec12```
* после чего выполняем:
```
pipenv shell
pipenv install django
pipenv install django-crispy-forms
```

### Шаг 1. Инициализация приложения ```articles```
Теперь нам необходимо приложение для работы с статьями.
```
python manage.py startapp articles
```
Приложение ```articles``` занимается менеджментом статьей (удаляет, создает, показывает и т.д.)

* Установим приложение для проекта : 
```
settings.py -> INSTALLED_APPS ->

INSTALLED_APPS = [
    'users.apps.UsersConfig', # Регистрация приложения
    'pages.apps.PagesConfig',
    'articles.apps.ArticlesConfig',
```

Пусть наша статья будет иметь представление о том, когда она была создана. Для того, чтобы корректно работать с датами необходимо подсказать ```Django``` какой часовой пояс мы выбираем.
Мы находимся в ```Europe/Moscow```, соответственно подскажем ```Django``` что нужно считат ьвремя относительно этого часового пояса.
```
# settings.py
....
TIME_ZONE = 'Europe/Moscow'
```

### Шаг 2. Инициализация модели Article
Создадим модель статьи ```Article```:
```
# articles/models.py

from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model # данная функция отдает текущую пользовательскую модель

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('detail_article', args=[str(self.id)])
```

* Подготовим миграционные запросы : ```python manage.py makemigrations articles```
* Применим миграции ```python manage.py migrate```



### Шаг 3. Регистрация модели для интерфейса админа
Зарегистрируем модель ```Article``` в интерфейсе админа:
```
# articles/admin.py

from django.contrib import admin
from .models import Article


admin.site.register(Article)

```

### Шаг 4. Запуск
* ```python manage.py runserver```
* Создадим пару-тройку статей в интерфейсе админа
