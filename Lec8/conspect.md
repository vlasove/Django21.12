## Лекция 8. Аккаунтинг (стандартный).

***Проблема:*** есть функционал сторонней модели, но полностью отстуствует функционал для пользователськой модели. 

***Задача:*** реализовать механизмы аутентификации и авторизации , используя стандартные ```django```-приложения (стандартную ```Django``` модель пользователя).


***Аутентификация*** - это процесс узнавания "свой-чужой". (С аутентификацией связаны процедуры ```Log In``` (войти в центр), ```Log Out``` (выйти из центра, сообщить, что вы ушли)).


***Авторизация*** - это процесс выдачи прав доступа. (С авторизацией связан процесс ```Register```)

### Шаг 0. Немного про стандартного пользователя
Стандартный юзер состоит из следующих атрибутов:
```
class User(....):
    username = ....
    password = ....
    email = .....
    first_name = ....
    last_name = ....
    is_authenticated = True/False 
    is_stuff = True/False
```

### Шаг 1. Подключение стандартного механизма ```Log In```:
На уровне нашего проекта в ```project/urls.py``` подключим стандатные процедуры аккаунтинга:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")), # Процесс передачи управления стандартному приложению
    path("", include("blog.urls")),
]

```

В данном приложении ```django.contrib.auth``` уже реализованы все ```url``` запросы и проставлены все отображения. От нас требуется только создать шаблоны.

Стандартный ```LoginView``` приложения ```django.contrib.auth``` выглядит примено так:
```
class LoginView(....):
    model = ....
    template_name = "register/login.html"
```

Создадим шаблон ```templates/registration/login.html```, который будет подтягиваться стандартным ```LoginView```:
```
<!--templates/registration/login.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Log In Page</h2>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p}}
        <button type="submit">Log In</button>
    </form>
{% endblock content %}
```

Теперь сообщим ```Django``` куда перенаправлять пользователя, в случае успешного ```Log In```.
Для этого зайдем в ```project/settings.py``` и в самом конце файла добавим :
```

# Для реализации логин/логаут
LOGIN_REDIRECT_URL = "home"

```

### Шаг 2. Добавление в базовый шаблон информации про успешную аутентификацию.
На данный момент после прохождения прцоедуры ```Log In``` клиенту не понятно, залогинен ли он, или нет. Создадим следующий функционал. Если пользователь залогинен - наверху будем выводить ```Hi, <USERNAME>. You are logged in!``` , в противном случае ```You are not logged in. <Log In>```.

Для этого заходим в ```templates/base.html```:
```
...
        <header>
            <h1>
                <a href="{% url 'home' %}">Home Page</a>
                 |
                <a href="{% url 'new_post' %}">+ New Blog Post</a> 
            </h1>
        </header>
        <!--Тут будет про логин-->
        {% if user.is_authenticated %}
            <p>Hi, {{ user.username }}. You are loggend in!</p>
        {% else %}
            <p>You are not logged in.</p>
            <a href="{% url 'login'%}">Log In</a>
        {% endif %}
...
```

Проверим, что все работает: ```python manage.py runserver```


### Шаг 3. Log Out
Теперь мы можем войти ```Log In```, но не можем выйти ```Log Out```. Реализовать ```Log Out``` очень просто. Для этого нужно:
* В ```templates/base.html``` доабвим ссылку на ```logout```:
```
        {% if user.is_authenticated %}
            <p>Hi, {{ user.username }}. You are loggend in!</p>
            <a href="{% url 'logout' %}">Log Out</a>
        {% else %}
```
* Нужно определить, куда пользователя перенаправлять после прохождения ```logout```. Для этого заходим в ```project/settings.py``` в самый низ:
```
# Для реализации логин/логаут
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
```

### Шаг 4. Механизм ```Sign Up```
В стандартном приложении ```django.contrib.auth``` есть много чего интересного (```login, logout, password_reset, password_change```), но отсутствует механизм регистрации ```signUp```.
Мы же решим эту проблему следующим образом:
* Создадим новое приложение ```python manage.py startapp accounts```
* Зарегистрируем это приложение (```settings.py -> INSTALLED_APPS-> ''accounts.apps.AccountsConfig','```)
* Когда проект передает работу нашему приложению? ```project/urls.py```:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")), # Процесс передачи управления стандартному приложению
    path("", include("blog.urls")),
]
```

* Определим пару ```url-отображение``` на уровне ```accounts/urls.py```:
```
from django.urls import path 

from .views import SignUpView 

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
```

* Теперь создадим отображение ```SignUpView```:
```
from django.views.generic import CreateView
from django.urls import reverse_lazy
# Стандартный интерфейс взаимодействия со стандартным пользователем
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

```

* Реализуем шаблон ```templates/signup.html```:
```
<!--templates/signup.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Sign Up Page</h2>
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Sign Up</button>
    </form>
{% endblock content %}
```

* Проверим, что все работает : ```python manage.py runserver```