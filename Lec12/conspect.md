## Лекция 12. Полный аккаунтинг

***Проблема:*** механизмы ```login/logout/signup``` - это не полные механизмы ```user-accounting``` , которые по стандарту должны быть реализованы. Для того, чтобы сделать минимальный набор функционала пользователя необходмио еще поддерживать операции ***смены*** и ***сброса*** пароля.

### Шаг 1. Инициализация проекта.
* Копируем содержимое проекта из прошлой лекции
* Если не переносили файлы окружения:
```
pipenv shell
pipenv install django
pipenv install django-crispy-forms
```

### Шаг 2. А что есть из стандартного?
Перейдем на страничку ```localhost:8000/users/``` и увидим следующее:
```
Using the URLconf defined in project.urls, Django tried these URL patterns, in this order:

admin/
users/ signup/ [name='signup']
users/ login/ [name='login']
users/ logout/ [name='logout']
users/ password_change/ [name='password_change']
users/ password_change/done/ [name='password_change_done']
users/ password_reset/ [name='password_reset']
users/ password_reset/done/ [name='password_reset_done']
users/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
users/ reset/done/ [name='password_reset_complete']
[name='home']
```

***Вывод*** оказывается механизмы смены и сброса пароля уже реализованы при помощи стандартного приложения ```django.contrib.auth``` (точно также как и ```login, logout```).

***Замечание:*** перед переходом на страницу ```users/password_change/``` необходимо пройти процедуру ```login``` за любого пользователя.


Но есть проблема - шаблон, отображемый на странице ```users/password_change/``` - стандартный. Данный шаблон используется в панели администратора и содержит в себе ряд ссылок, что не очень хорошо - предоставлять клиенту доступ к этим ссылкам.

***Решение*** подменим шаблоны для ```password_change``` и ```password_change/done```.

### Шаг 3. Подмена шаблонов для изменения пароля
* Создадим:
```
templates/registration/password_change_form.html
templates/registration/password_change_done.html
```
* Зайдем в ```templates/registration/password_change_form.html```
```
<!--templates/registration/password_change_form.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Password Change Page</h1>
    <p>Please enter your old password, for security reasons, then enter twice new password.</p>

    <form method="POST">
        {% csrf_token %}
        {{ form|crispy }}

        <button class="btn btn-success" type="submit">Change My Password</button>
    </form>

{% endblock content %}
```

* Зайдем в ```templates/registration/password_change_done.html```
```
<!--templates/registration/password_change_done.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Password change successful!</h1>
    <p>Your password was changed.</p>
{% endblock content %}
```

***В итоге*** как оказалось, механизм смены пароля уже реализован одним из стандартных приложений ```django```. Нам же оставалось только изменить шаблоны, которые отображаются на ключевых страницах ```users/password_change/``` и ```users/password_change/done/```.


### Шаг 4. Реализация механизма сброса пароля
* Клиент заходит на веб-страницу
* Жмет ***сбросить пароль*** (не важно, залогинен он или нет)
* Вводит свой адрес электронной почты (номер телефона, номера гаража, номер почтового отделения)
* Присылыаем ссылку на страницу сброса ***КОНКРЕТНОГО АККАУНТА***
* Вводим 2 раза новый пароль

* ***НО ТУТ*** происходит главный вопрос. Что будет находится в бд все это время? Пока человек не прошел по ссылке и не ввел 2 раза новй пароль (подтвердив кнопкой ```submit``` ) мы не делаем никаих изменний в бд.

#### Шаг 4.1. Созададим юзера с полем - email
* Перейдем на страницу ```signup``` и создадим какого-нибудь пользователя с явно указанным адресом электронной почты (его ввод ранее мы трактовали как необязательный, поэтому для успешной работы механзима сброса нам нужен один юзер, на котором мы будем все проверять).

* Преподаватель создал юзера:
```
username : alice
password : 12345678qwerty
email : alice@gmail.com
age : 22
```

#### Шаг 4.2. Подскажем Django куда выбрасывать сгенерированную ссылку для сброса пароля
В целях упрощения данной процедуры сброс пароля будет происходить через консоль (т.е. в консоль будет отправляться ссылка для сброса пароля юзера).

* Переходим в ```settigns.py```
```
# Через что мы сбрасываем пароль
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

* Попробуем сбросить пароль при помощи стандартного механизма:
```
1) /users/password_reset/ 
2) Вводим нужный адрес электронной почты (это адрес юзера)
3) Нас перенаправило на /users/password_reset/done/
4) Глянем в консоль. Видим ссылку
5) Копируем в адресную строку
6) Попадаем на страницу /users/reset/.../set-password/
7) Устанавливаем новый пароль
8) После чего попадаем на страницу /users/reset/done/
```

***В итоге*** у нас есть 4 различные веб-страницы, для которых нам необходимо создать новые шаблоны:
```
templates/registration/password_reset_form.html
templates/registration/password_reset_done.html
templates/registration/password_reset_confirm.html
templates/registration/password_reset_complete.html
```
```
<!--templates/registration/password_reset_form.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Forgot your password?</h1>
    <p>Enter your email address below, we'll send you instructions</p>

    <form method="POST">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success" type="submit">Send me instructions!</button>
    </form>
{% endblock content %}
```


```
<!--templates/registration/password_reset_done.html-->
{% extends 'base.html' %}

{% block content %}
    <h1>Check your email inbox.</h1>
    <p>We've emailed you instructions for password resetting.</p>
{% endblock content %}
```


```
<!--templates/registration/password_reset_confirm.html-->
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block content %}
    <h1>Set new password</h1>
    <form method="POST">
        {% csrf_token %}
        {{ form|crispy }}
        <button class="btn btn-success" type="submit">Change Password</button>
    </form>
{% endblock content %}
```