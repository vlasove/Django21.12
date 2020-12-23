## Лекция №7. Веб-формы.

***Проблема:*** для того, чтобы взаимодействовать с моделью мы должны заходить в панель адмнинистратора - это плохо и неудобно. Хотим сделать первичный пользовательский функционал, для того, чтобы любой юзер мог взаимодействовать с моделью (создавать новые посты, обновлять имеющиеся, удалять имеющиеся).

***Задача:*** создать (или воспользоваться существующими) механизмами взаимодействия с моделью.

***Интерфейс*** - контракт (что можно делать с каким-либо объектом).

***Форма (взаимодействия)*** - конкретная реализация интерфейса (напрмиер, можно создать объект, можно удалить объект, можно обновить информацию про объект). Говорят, что форма взаимодействия задана - если реализована часть какого-либо интерфейса.

***Веб-форма (взаимодействия)*** - конкретная реализация интерфейса в виде веб-страницы.

### Шаг 1. Изменим имеющийся ```base.html```
Переходим в ```templates/base.html``` и вносим туда следующие изменения:
```
...
<header>
            <h1>
                <a href="{% url 'home' %}">Home Page</a>
                 |
                <a href="{% url 'new_post' %}">+ New Blog Post</a> 
            </h1>
        </header>

```
### Шаг 2. Определим ```new_post```
Поскольку сейчас нам необходимо реализовать новую пару взаимодействий запрос-отображение мы переходим в ```blog/urls.py```:
```
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView

urlpatterns = [
    path("post/new/", BlogCreateView.as_view(), name = "new_post"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="detail_post"),
    path("", BlogListView.as_view(), name="home"),
]
```

### Шаг 3. Создадим ```BlogCreateView```
Переходим в ```blog/views.py```:
```
from django.views.generic import ListView , DetailView, CreateView
....
class BlogCreateView(CreateView):
    model = Post 
    template_name = "new_post.html"
    fields = '__all__' # какие поля мы будем заполнять в веб-форме
```

### Шаг 4. Реализация шаблона ```new_post.html```
* Создаем шаблон ```templates/new_post.html```
```
<!--templates/new_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>New Post</h1>
    <!--Здесь начинается веб-форма-->
    <form action="" method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <!--Подтверждение формы-->
        <input type="submit" value="Create" />
    </form>
{% endblock content %}
```

### Шаг 5. Проверим, что все работает
* ```python manage.py runserver```
* Попробуем создать новый пост через веб-форму
* Все падает - печально
* Попробуем разрешить эту ситацию.

### Шаг 6. Добавление абсолютного перенаправления после взаимодействий
Определим метод ```get_absolute_url(self)``` на уровне модели, который будет перенаправлять пользователя на ```detail_post``` во всех ситациях (пользователь создал пост - покажи ему созданный пост детально, пользователь обновил пост - покажи пользователю обновленный пост детально).

Данный метод определяется на уровне модели, поэтому мы переходим в ```blog/models.py```:
```
from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        'auth.User', # дефолтынй пользователь из django.contrib.auth
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        """
        Хотим перенаправлять на ```DetailView``` данного поста
        """
        return reverse("detail_post", args=[str(self.id)])
```