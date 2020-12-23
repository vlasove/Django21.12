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

### Шаг 7. Форма для обновления поста
Расширим реализацию интерфейса взаимодействия с моделью при помощи веб-формы для обновления содержимого поста.
Для этого:
* Заходим в ```detail_post.html```:
```
.....
    </div>
    
    <a href="{% url 'update_post' post.pk %}">+ Update Post</a>
{% endblock content %}
```

* Создадим шаблон для обновления ```templates/update_post.html```:
```
<!--templates/update_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Update this Post</h1>
    <form action="" method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Update" />
    </form>
{% endblock content %}
```

* Создадим ```UpdateView``` , который будет вызывать шаблон:
```
from django.views.generic import UpdateView
....

class BlogUpdateView(UpdateView):
    model = Post 
    template_name = "update_post.html"
    fields = ['title', 'body'] # поля, которые я хочу обновлять
```

* Создадим пару ***запрос-отображение***, для этого переходим в ```blog/urls.py```:
```
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView

urlpatterns = [
    path("post/<int:pk>/update/", BlogUpdateView.as_view(), name="update_post"),

    
    path("post/new/", BlogCreateView.as_view(), name = "new_post"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="detail_post"),
    path("", BlogListView.as_view(), name="home"),
]
```

* Проверим, что все работает : ```python manage.py runserver```

### Шаг 8. Форма удаления поста
* Заходим в шаблон ```detail_post.html```:
```
    </div>
    
    <a href="{% url 'update_post' post.pk %}">+ Update Post</a>
    |
    <a href="{% url 'delete_post' post.pk %}">- Delte Post</a>
{% endblock content %}
```
* Создадим шаблон для удаления поста ```templates/delete_post.html```:
```
<!--templates/delete_post.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Delete this Post</h1>
    <form action="" method="POST">
        {% csrf_token %}
        <p>Are you sure you want to delete this post></p>
        <input type="submit" value="Confirm"/>
    </form>
{% endblock content %}
```

* Создадим новое отображение ```DeleteView```. При создании и обновлении постов мы редиректим клиента на детальное отображение (это работает модельный метод ```get_absolute_url```). Но в случае удаления поста - детального отображения никакого показать не получится, поэтому рекомендуется установить редирект на уровне отображения, чтобы перебрасывать людей на домашнюю страницу. Но перебрасывать нужно только после того, как клиент сделать все действия на странице!
```
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

.....
class BlogFeleteView(DeleteView):
    model = Post 
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")
```

* Создадим новую пару ```url-отображение```. Для этого перейдем в ```blog/urls.py```:
```
from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView,BlogDeleteView

urlpatterns = [
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name = "delete_post"),
    path("post/<int:pk>/update/", BlogUpdateView.as_view(), name="update_post"),
    path("post/new/", BlogCreateView.as_view(), name = "new_post"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="detail_post"),
    path("", BlogListView.as_view(), name="home"),
]
```