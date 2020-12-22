## Лекция №3. Простейший многостраничный сайт

***Задача***: создать простейший многостраничный проект (поддерживает несколько ```URL``` запросов)

### Шаг 1. Инициализация проекта и окружения
* ```pipenv shell```
* ```pipenv install django```
* ```django-admin startproject project .```
* ```python manage.py startapp pages``` - создание приложения, показывающего несколько веб-страниц.

### Шаг 2. Регистрация приложения для проекта
* Заходим в файл ```project/settings.py``` -> ```INSTALLED_APPS``` ->
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig', # Регистрация приложения
]
```
* Проверим, что все работает : ```python manage.py runserver```

### Шаг 3. Шаблоны.
Исконно в идеоматике ```Django``` считается правильным следующий подход:
***Набор шаблонов у каждого приложения - свой***. Что это значит?
```
pages ->
        templates ->
                    pages ->
                            home.html
                            login.html
                            info.html
                            index.html

posts ->
        templates ->
                    posts ->
                            detail_post.html
                            create_post.html
                            update_post.html
```

Мы же на курсе (в целях упрощения жизни и ускорения работы) будем использовать ***одну*** директорию шаблонов на весь проект.

Для этого в корне рабочей директории (Lec3) создадим папку ```templates```.
Создадим ```templates/home.html```.

### Шаг 4. Подскажем Django, где теперь искать шаблоны
Для того, чтобы сообщить ```Django``` , где теперь будут находиться шаблоны, необходимо:
* Открыть файл ```project/settings.py```
* В самом начале файла импортируем : ```import os```
* В том же модуле находим список ```TEMPLATES```:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")], # ДОБАВИЛИ
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Шаг 5. Описание шаблона ```home.html```
Для описания шаблона ```templates/home.html``` заполним его следующим кодом:
```
<!-- templates/home.html -->

<h1>Home Page!</h1>
```

### Шаг 6. Классовое отображение
По скольку ```Django``` - шаблонизированный фреймворк, скорее всего в нем существует целый ряд заготовок для взаимодействия с отображениями. Для того, чтобы им воспользоваться - нам нужен механизм ***наследования***. ***Наследование*** поддерживается только классами. ***Вывод***: перепишем наши отображения с помощью классов и унаследуемся от стандартных ```View```.
Заходим в ```pages/views.py```:
```
from django.shortcuts import render
# Стандартный шаблон-отображение статической страницы
from django.views.generic import TemplateView 

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"
```

### Шаг 7. Обращение к новому View
Создадим файл ```pages/urls.py``` со следующим содержимым:
```
from django.urls import path 
from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view())
]
```

### Шаг 8. Передача работы приложению ```pages```
Заходим в ```project/urls.py```:
```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")), # добавление передачи управления приложению
]

```

### Шаг 9. Убедимся, что все работает
* ```python manage.py runserver```

### Шаг 10. Добавление второй веб-страницы
* Создаем шаблон ```templates/about.html```
```
<!--templates/about.html-->
<h1>About Page!</h1>
<p>This is second web-page!</p>
```

* Теперь создадим отображение, показывающее этот шаблон ```pages/views.py```:
```
.......
class AboutPageView(TemplateView):
    template_name = "about.html"

```

* Теперь опишем правило вызова нового отображения: ```pages/urls.py```
```
from django.urls import path 
from .views import HomePageView, AboutPageView

urlpatterns = [
    path("about/", AboutPageView.as_view()),
    path("", HomePageView.as_view()),
]
```

* Проверим, что все работает : ```python manage.py runserver```


### Шаг 11. Простейшее наследование шаблонов
* Создадим базовый шаблон ```templates/base.html```:
```
<!--templates/base.html-->
<header>
    <a href="/">Home</a> | <a href="/about">About</a>
</header>

<!--Синтаксис шаблонизатора-->
{% block conent %}
{% endblock content %}
```

*  Теперь унаследуемся от ```base.html``` внутри ```home.html```:
```
<!-- templates/home.html -->
{% extends 'base.html' %}

{% block content %}
    <h1>Home Page!</h1>
{% endblock content%}
```
* Аналогично поступим с ```about.html```
```
<!--templates/about.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>About Page!</h1>
    <p>This is second web-page!</p>
{% endblock content %}
```
