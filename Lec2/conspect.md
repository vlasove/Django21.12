## Лекция 2. Hello-Web!

***Задача***: создадим простейшее приложение в стиле ```hello-web```!

### Шаг 1. Подготовка
* Создаю окружение ```pipenv shell```
* Устанавливаю в это окружение ```django```: ```pipenv install django```
* Инициализирую проект : ```django-admin startproject project .```
* Проверю, что все работает ```python manage.py runserver```
* Вижу летающую ракету - все работет. Жмем ```Ctrl + C```.

### Шаг 2. Создание первого приложения

***Замечание***: ```django``` поддерживает следующий способ проектирования :
* создается исходный проект
* проект является способ окрестрирования приложений
* приложения выполняют полезную работу

Для того, чтобы создать первое приложение , ***задачей которого будет вывод сообщения Hello Web!!***, создадим свое первое приложение:
```
python manage.py startapp <application_name>
```

### Шаг 2.1. Регистрация приложения
Сообщим проекту, что вместе с ним теперь работает новое приложение. Для этого:
* заходим в ```settings.py```
* Ищем список ```INSTALLED_APPS```
* Добавляем информация про то, что мы хотим подцепить наше приложение к проекту (процесс регистрации)
```
INSTALLED_APPS = [
    'pages.apps.PagesConfig', # в этом месте мы подцепляем приложение к проекту
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
* Смотрим, что все не сломалось: ```python manage.py runserver```

### Шаг 2.2. Отображения. Это кто?
Типичный цикл работы связки ```request/response``` в Django выглядит следующим образом:
```
URL -> View -> Model (не всегда) -> Template
```
* ```URL``` - запрос адресной строки
* ```View``` - правило отображения. Знает про то, где данные взять и как их распихать по шаблонам.
* ```Model``` - правила взаимодействия с Базой Данных.
* ```Template``` - ```html```- шаблон, в который скорее всего будут вставлены какие-то данные.


Создадим свое первое самое простое отображение.
* Заходим в приложение ```pages/views.py```
```
#pages/views.py
from django.http import HttpResponse, HttpRequest

# Создадим свое первое отображения.
# Все отображения(в виде функций) принимают один аргумент - request
def homePageView(request:HttpRequest):
    """
    Возвращает убогую гадость с надписью `Hello Web!`
    """
    return HttpResponse("Hello Web!")
```
* Теперь опишем правило выбора нашего отображения. Внутри приложения ```pages``` создадим файл ```urls.py```. Данный файл будет содержать в себе информацию про то, в какой ситуации какое отображение вызывать.
```
#pages/urls.py
from django.urls import path 
from .views import homePageView

# Название этого списка СТАНДАРТИЗИРОВАНО!!!!!
urlpatterns = [
    path("", homePageView)
]
```

* Теперь сообщим нашему проекту, в какой ситуации мы отдаем работу созданному приложению. Для этого зайдем в файл ```project/urls.py```.
```
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("pages/", include("pages.urls")),
]

```

* Запустим и проверим, как это работает: ```python manage.py runserver```