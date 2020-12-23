## Лекция 10. Аккаунтинг на CustomUser

***Задача:*** реализовать механизмы аккаунтинга (```login, logout, signup```) применимо к модели ```CustomUser```.


### Шаг 1. Инициализация шаблонов
* Создадим следующий набор шаблонов:
```
templates/registration/login.html
templates/base.html
templates/home.html
templates/signup.html
```
* Подскажем ```Django``` где искать шаблоны:
```
settings.py -> TEMPLATES -> "DIRS" : [os.path.join(BASE_DIR, "templates")],
```
* Сразу опишем, куда перенаправляем пользователя в случае успешного ```login/logout```: 
```
#project/settings.py в самом низу

.......
# Куда редиректимся в случае логни/логаут
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

### Шаг 2. Наполнение шаблонов
* ```templates/base.html```
```
<!--templates/base.html-->
<html>
    <head>
        <title>Django Blog App</title>
    </head>

    <body>
        <main>
            {% block content %}
            {% endblock content %}
        </main>
    </body>
</html>
```

* ```templates/home.html```
```
<!--templates/home.html-->
{% extends 'base.html' %}


{% block content %}
    {% if user.is_authenticated %}
        <p>Hi, {{ user.username }}</p>
        <p>
            <a href="{% url 'logout' %}">Log Out</a>
        </p>
    {% else %}
        <p>You are not logged in.</p>
        <a href="{% url 'login' %}">Log In</a>
        |
        <a href="{% url 'signup' %}">Sign Up</a>
    {% endif %}
{% endblock content %}
```

* ```templates/registration/login.html```
```
<!--templates/registration/login.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Log In Page</h2>
        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Log In</button>
        </form>
{% endblock content %}
```

* ```templates/signup.html```
```
<!--templates/signup.html-->
{% extends 'base.html' %}

{% block content %}
    <h2>Sign Up Page</h2>
    <form method="POST">
        {% scrf_token %}
        {{ form.as_p }}
        <button type="submit">Sign Up</button>
    </form>
{% endblock content %}
```

# Шаг 3. Определение процесса передачи работы 
На уровне ```project/urls.py``` опишем следующую логику:
* механизмы ```login/logout``` пусть выполняет стандартное приложение ```django.contrib.auth``` с использованием ```CustomUser```
* механизм ```signup/``` будет проходить через приложение ```users.urls```
* механизм показа домашней страницы - делегируем отдельному приложению ```pages```

```
# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")), # передача signup
    path("users/", include("django.contrib.auth.urls")), # использование login/logout
    path("", include("pages.urls")), # приложение для показа домашней страницы
]

```

* Создадим приложение ```pages``` : ```python manage.py startapp pages```
* Зарегестрируем это приложение ```settings.py -> installed_apps...```
* Определим в ```pages/urls.py``` следующее:
```
from django.urls import path 
from .views import HomePageView


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]
```
* Определеим в ```pages/views.py```
```
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomePageView(TemplateView):
    template_name = "home.html"

```

* Определеим в ```users/urls.py```:
```
from django.urls import path 
from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
```

* Теперь создадим ```SignUpView``` в ```users/views.py```
```
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy 

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

```

***ВАЖНО***: для того, чтобы на этапе регистрации (в веб-форме ```signup.html```) запросить нужные нам поля, изменим содержание необходимых полей в формах ниже ```users.forms.py```
```
from .models import CustomUser

# Заготовки интерфейса пользовательской модели
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    """
    Наш интерфейс взаимодействия с нашей CustomUser моделью
    Создание юзера
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'age')



class CustomUserChangeForm(UserChangeForm):
    """
    Наш интерфейс взаимодействия с нашей CustomUser моделью
    Редактирование юзера
    """
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields =  ('username', 'email', 'age') 
```
***Примечание*** : пароли всегда заправшиваются в любом случае!