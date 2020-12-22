## Лекция 6. Индивидуальные страницы и СТИЛЬ

***Проблема***: модель очень упрощена и кажется, что все очень легко. Хотим немного усложнить модель, также хотим сделать индивидуальные страницы для каждого поста и еще хочу сделать стильно.


### Шаг 1. Инициализация проекта
* ```pipenv shell```
* ```pipenv install django```
* ```django-admin startproject project .```
* ```python manage.py startapp blog```
* ```python manage.py migrate```
* ```settings.py``` -> ```INSTALLED_APPS``` -> ```'blog.apps.BlogConfig'```
* ```python manage.py runserver```

### Шаг 2. Описание модели данных
***Хотелки*** пусть у постов будут такие поля:
* название поста
* тело поста
* автор поста ?????!!!!!!!!

Если возникает автор поста, то получается в нашем приложении существует реляция между моделями ```Post``` и ```DefaultUser```.
Существует 4 типа отношений:
* один к одному (```One-to-One```) : человек и его серия/номер_паспорта
* многие ко многим (```Many-to-Many```) : студент и студенческие общины
* один ко многим (```One-to-Many```) : профессор и его дипломники
* многие к одному


В данной задаче выбираем типы реляции - ```One-to-Many```, т.к. у одного автора может быть неограничено число постов, а у одного поста - не может быть более одного автора (и менее одного автора тоже нельзя).

```
# blog/models.py
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    body = model.TextField()
    author = models.ForeignKey(
        'auth.User', # дефолтынй пользователь из django.contrib.auth
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.title 
```

* Подготовим миграционные запросы: ```python manage.py makemigrations blog```
* Применим миграционные запросы: ```python manage.py migrate blog```

### Шаг 3. Добавление модели в панель администратора
* Создадим суперпользователя ```python manage.py createsuperuser```
* Зарегестрируем модель в интерфейсе админа:
```
# blog/admin.py
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```
* Зайдем в панель админа и создадим 3-4 поста.


### Шаг 4. Связываем запросы и отображения
* На уровне проекта ```project/urls.py```
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls")),
]

```
* На уровне приложения ```blog/urls.py```:
```
from django.urls import path
from .views import BlogListView

urlpatterns = [
    path("", BlogListView.as_view(), name="home"),
]
```

* На уровне ```blog/views.py```:
```
from django.shortcuts import render
from django.views.generic import ListView 
from .models import Post 
# Create your views here.

class BlogListView(ListView):
    model = Post 
    template_name = "home.html"
    context_object_name = "posts"

```

### Шаг 5. Шаблоны
* Создадим файлы ```templates/base.html``` и ```templates/home.html```
* Подскажем ```Django``` где искать шаблоны :
```
settings.py -> TEMPLATES -> "DIRS" : [os.path.join(BASE_DIR, "templates")],
```
* Опишем ```base.html```
```
```