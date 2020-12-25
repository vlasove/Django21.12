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


### Шаг 4. Детальное отображение статьи
```
# articles/urls.py
from django.urls import path 

from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path("<int:pk>/", ArticleDetailView.as_view(), name="detail_article"), # articles/3/
    path("", ArticleListView.as_view(), name="list_articles"), #
]
```

```
#articles/views.py
from django.views.generic import ListView , DetailView
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "list_articles.html"
    context_object_name = "list_articles"


class ArticleDetailView(DetailView):
    model = Article 
    template_name = "detail_article.html"
    context_object_name = "article"

```
```
<!--templates/detail_article.html-->
{% extends 'base.html' %}

{% block content %}
    <div class="article-entry">
        <h2>{{ article.title }}</h2>
        <p>by {{ article.author }} | {{ article.date }}</p>
        <p>{{ article.body }}</p>
    </div>
    <p>
        <a href="{% url 'update_article' article.pk %}">Edit</a>
        |
        <a href="{% url 'delete_article' article.pk %}">Delete</a>
    </p>
    <p>Back to
        <a href="{% url 'list_articles' %}">All Articles</a>
    </p>
{% endblock content %}
```

### Шаг 5. Обновление статьи
```
# articles/urls.py
from django.urls import path 

from .views import ArticleListView, ArticleDetailView, ArticleUpdateView

urlpatterns = [
    path("<int:pk>/", ArticleDetailView.as_view(), name="detail_article"), # articles/3/
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name= "update_article"), # articles/2/update/
    path("", ArticleListView.as_view(), name="list_articles"), #
]
```

```

#articles/views.py
from django.views.generic import ListView , DetailView, UpdateView
from .models import Article


class ArticleUpdateView(UpdateView):
    model = Article 
    fields = ("title", "body")
    template_name = "update_article.html"
    
```

```
<!--templates/update_article.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Update Article</h1>
    <form action="" method="POST">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-info ml-2" type="submit">Update</button>
    </form>

{% endblock content %}
```

### Шаг 6. Удаление статьи
```
# articles/urls.py
from django.urls import path 

from .views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path("<int:pk>/", ArticleDetailView.as_view(), name="detail_article"), # articles/3/
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name= "update_article"), # articles/2/update/
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name= "delete_article"), 
    path("", ArticleListView.as_view(), name="list_articles"), #
]
```


```
#articles/views.py
from django.views.generic import ListView , DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .models import Article

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "delete_article.html"
    success_url = reverse_lazy("list_articles")
```

```
<!--templates/delete_article.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Delete Article</h1>
    <form method="POST" action="">
        {% csrf_token %}
        <p>Are you sure you want to delete this article?</p>
        <button class="btn btn-danger ml-2" type="submit">Delete</button>
    </form>
{% endblock content %}
```

### Шаг 7. Редактирвоание ```list_articles.html```
```
...
            <div class="card-footer text-center text-muted">
                <a href="{% url 'update_article' article.pk %}">Edit</a> 
                | 
                <a href="{% url 'delete_article' article.pk %}">Delete</a>
            </div>
...
```

### Шаг8. Запуск и ручные тесты Crud
* ```python manage.py runserver```
* Посмотрим, что все работает