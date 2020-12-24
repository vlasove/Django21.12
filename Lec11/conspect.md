## Лекция 11. Стилизация и Bootstrap

***Проблема:*** до сих пор мы пользовались обычной связкой ```.py``` <-> ```.html```.  Стандартно ```html``` отвечают только за расположение блоков на веб-странице (скелет веб-страницы). Внешний вид задают ```.css``` файлы. 

***Задача:*** сделать стильно.


### Шаг 1. Где живут ```css``` фреймворки?
Одним из популярных ```css```- фреймворков является ***Bootstrap***.
Найти его можно тут: https://getbootstrap.com/.

Основное преимущество ```Boostrap``` состоит в ***адаптивности***.

***Адаптивность (адаптивный дизайн)*** - расположение стилизации и ключевых элементов на веб-странцие, привязанных не к конкретным пикселям, а к расположению элементов относительно ***РАСШИРЕНИЯ*** веб-страницы.

* Заходим на страницу https://getbootstrap.com/docs/5.0/getting-started/introduction/
* Копируем шаблон ```starter template``` в любой ```.html``` файл
* Откроем данный файл в браузере


* Теперь попроуем усложнить шаблон.
```
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Моя кнопка</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
      
          <div class="collapse navbar-collapse" id="navbarsExampleDefault">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
              <li class="nav-item active">
                <a class="nav-link" aria-current="page" href="#">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Link</a>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="dropdown01" data-bs-toggle="dropdown" aria-expanded="false">Dropdown</a>
                <ul class="dropdown-menu" aria-labelledby="dropdown01">
                  <li><a class="dropdown-item" href="#">Action</a></li>
                  <li><a class="dropdown-item" href="#">Another action</a></li>
                  <li><a class="dropdown-item" href="#">Something else here</a></li>
                </ul>
              </li>
            </ul>
            
          </div>
        </div>
      </nav>
      
      
      <div>
          <p>Здесь будет наш контент</p>
      </div>
      
      

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js" integrity="sha384-q2kxQ16AaE6UbzuKqyBE9/u/KzioAlnx2maXQHiDX9d4/zp8Ok3f+M7DPm+Ib6IU" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.min.js" integrity="sha384-pQQkAEnwaBkjpqZ8RU1fF1AKtTcHJwFl3pblpTlHXybJjHpMYo79HY3hIi4NKxyj" crossorigin="anonymous"></script>
    
  </body>
</html>
```

* Теперь мы переделаем данный шаблон под наше приложение. Нам нужны блоки для перехода на новую страничку и панелька для Login/Logout/SignUp. Переходим в шаблон ```templates/base.html```:

```
<!-- templates/base.html -->
<!doctype html>
<html lang="en">
<head>
<!-- Required meta tags -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,
initial-scale=1, shrink-to-fit=no">
<!-- Bootstrap CSS -->
<link rel="stylesheet"
href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/\
bootstrap.min.css"
integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81i\
uXoPkFOJwJ8ERdknLPMO"
crossorigin="anonymous">
<title>{% block title %}Django Blog App{% endblock title %}</title>
</head>
<body>
<nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
  <a class="navbar-brand" href="{% url 'home' %}">Django Blog App</a>
    {% if user.is_authenticated %}
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a href=""> <!--Здесь добавим ссылку на создание поста-->
            + New
          </a>
        </li>
      </ul>
    {% endif %}
<button class="navbar-toggler" type="button" data-toggle="collapse"
data-target="#navbarCollapse" aria-controls="navbarCollapse"
aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="navbarCollapse">
{% if user.is_authenticated %}
<ul class="navbar-nav ml-auto">
<li class="nav-item">
<a class="nav-link dropdown-toggle" href="#" id="userMenu"
data-toggle="dropdown" aria-haspopup="true"
aria-expanded="false">
{{ user.username }}
</a>
<div class="dropdown-menu dropdown-menu-right"
aria-labelledby="userMenu">
<a class="dropdown-item" href="{% url 'password_change' %}">Change password</a>
<div class="dropdown-divider"></div>
<a class="dropdown-item" href="{% url 'logout' %}">Log Out</a>
<div class="dropdown-divider"></div>
<a class="dropdown-item" href="{% url 'password_reset' %}">Password Reset</a>
</div>
</li>
</ul>
{% else %}
<form class="form-inline ml-auto">
<a href="{% url 'login' %}" class="btn btn-outline-secondary">
Log In</a>
<a href="{% url 'signup' %}" class="btn btn-primary ml-2">
Sign up</a>
</form>
{% endif %}
</div>
</nav>
<div class="container">
{% block content %}
{% endblock content %}
</div>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4\
YfRvH+8abtTE1Pi6jizo"
crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/\
1.14.3/
umd/popper.min.js"
integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbB\
JiSnjAK/
l8WvCWPIPm49"
crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/\
js/bootstrap.min.js"
integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ\
6OW/JmZQ5stwEULTy"
crossorigin="anonymous"></script>
</body>
</html>
```