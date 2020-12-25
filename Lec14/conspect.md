## Лекция 14. Реализация CrUD для модели Articles

***Проблема:*** у нас полный пользовательский функционал. Но пока мы умеем создавать объекты ```Article``` при помощи веб-форм. Нужно реализовать ```CrUD``` для модели.


### Шаг 1. Передача управления проектом приложению

Хотим прописать, когда проект передает управление приложению ```articles```.
```
# project/settings.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")), # передача signup
    path("users/", include("django.contrib.auth.urls")), # использование login/logout
    path("articles/", include("articles.urls")),
    path("", include("pages.urls")), # приложение для показа домашней страницы
]

```

### Шаг 2. Пропишем, какие пары ```url - отображение``` обрабатывает приложение ```articles```
Реализация таких пар происходит на уровне приложения в файле ```articles/urls.py```.
```
# articles/urls.py
from django.urls import path 


urlpatterns = [
    path(),
]
```

### Шаг 3. Реализуем отображение списка всех статей в сервисе
```
# articles/urls.py
from django.urls import path 

from .views import ArticleListView

urlpatterns = [
    path("", ArticleListView.as_view(), name="list_articles"),
]
```

```
#articles/views.py
from django.views.generic import ListView 
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "list_articles.html"
    context_object_name = "list_articles"

```
```
<!--templates/list_articles.html-->
{% extends 'base.html' %}

{% block content %}
    {% for article in list_articles %}
        <div class="card">
            <!--Шапка карточки статьи-->
            <div class="card-header">
                <span class="font-weight-bold">{{ article.title }}</span> 
                |
                <span class="text-muted">
                    by {{ article.author }} | {{article.date}}
                </span>
            </div>
            <!--Тело карточки статьи-->
            <div class="card-body">
                {{ article.body }}
            </div>
            <!--Подвал карточки статьи-->
            <div class="card-footer text-center text-muted">
                <a href="#">Edit</a> | <a href="#">Delete</a>
            </div>
        </div>
        <br/>
    {% endfor %}
{% endblock content %}
```