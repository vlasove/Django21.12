## Лекция 5. Создание простейшей модели данных

***Задача:*** разобраться как взаимодействовать нашему пиложению с моделью, которую мы опишем.
***Проблема***: что такое модель?

### Шаг 1. Модель - это ...
***Модель*** - это набор правил по взаимодействию программных объектов (сущностей) с базой данных.

Допустим, мы договорились, что будем хранить информацию про книгу следующим образом:
```
id | title | author | pages | price
```
Но в один прекрасный день, понадобилось модифицировать данную схему хранения:
```
id | title | author | pages | price | owner 
```

Как называется процесс ***перехода от одной схемы хранения данных к другой***?  - Это ***миграция***.

***Миграцией*** - называют процесс переход от одной схемы хранения данных к другой без утраты имеющейся инфомрации в БД.

Для того, чтобы выоплнить миграцию необходимо ***подготовить запросы по изменению схемы хранения данных в таблицах*** ( ```ALTER TABLE .......```) - ***подготовка миграции***.

***Миграция*** - это процесс применения запросов, подготовленных на предыдущем этапе.



### Шаг 2. Инициализация приложения.
***Хотелки***: хотим создать приложение в котором будет задана одна модель - ```Post``` (пост в блоге).

* ```pipenv shell```
* ```pipenv install django```
* ```django-admin startproject project .```
* ```python manage.py startapp posts```
* Заходим в ```project/settings.py``` -> ```INSTALLED_APPS``` - > 
```
INSTALLED_APPS = [
    'posts.apps.PostsConfig', # Регистрация приложения для проекта
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

```

### Шаг 3. Первичная миграция.
Для осуществления первичной миграции в ручном режиме необходимо выполнить команду:
```
python manage.py migrate
```
***Замечание***: на этом этапе нам не нужно подготавливать запросы по изменения структуры БД, т.к. они уже были подготовлены стандратными (встроенными) приложениями в ```Django```.


### Шаг 4. Создание первой модели ```Post```
Для создания первой модели переходим в приложение в ```posts/models.py```
```
from django.db import models

# Create your models here.
class Post(models.Model):
    text = models.TextField()

```

***Теперь*** подготовим запросы по изменению схемы текующей базы данных - подготовить миграцию.
```
python manage.py makemigrations posts
```

***После этого*** применим этим запросы:
```
python manage.py migrate posts
```

### Шаг 5. Django Admin
Для взаимодействия с моделью выберем самый простой путь - зайдем через панель администратора.
Для того, чтобы туда попасть необходимо создать пользователя с правами администратора:
```
python manage.py createsuperuser
```

Теперь запустим сервер ```python manage.py runserver``` и перейдем по адресу ```admin/```.

### Шаг 6. Регистрация модели в панели администратора
Для того, чтобы админ мог взаимодействовать с моделью ```Post``` из-под панели администратора, необходимо зайти в файл ```posts/admin.py```
```
from django.contrib import admin
from .models import Post
# Register your models here.

admin.site.register(Post)
```

Теперь в панели администратора доступна наша модель и есть проблема - после создания нового поста информация о нем очень криво отображается. Изменим это:
```
posts/models.py

from django.db import models

# Create your models here.
class Post(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

```

Миграции не подготавливаем потому что ***структура данных не менялась***.

### Шаг 7. Добавление моделей в шаблоны.
***Задача:*** вывести все объекты модели ```Post``` в ```html``` шаблон и показать его пользователю.

* Сначала определим правило отображения в файл ```posts/views.py```:
```
from django.views.generic import ListView 
from .models import Post

# Create your views here.

class HomePageView(ListView):
    model = Post 
    template_name = "home.html"
    context_object_name = "posts"
```

***ListView*** - стандартный способ отображения списком элементов модели.
```model``` - атрибут класса ```ListView```, отвечает за то- с какой моделью работаем.

* Создадим файл ```templates/home.html```
* Подскажем ```Django``` где искать шаблоны : ```settings.py``` -> ```TEMPLATES``` -> 
```
'DIRS': [os.path.join(BASE_DIR, "templates")],
```

* Наполним шаблон ```templates/home.html```
```
<!--templates/home.html-->
<h1>My Home Page</h1>
<ul>
    <!--Так в Jinja2 обозначается цикл for-->
    {% for post in posts %}
        <li>{{ post }}</li> <!--А вот так оформляется вставка элемента-->
    {% endfor %}
</ul>
```

***Замечание*** поле ```context_object_name``` в ```view``` обозначает имя, доступное внутри шаблона, по которому я могу полчать доступ к элементам модели.

* Сопоставим ```url``` запрос с нашим отображением:
```
#posts/urls.py
from django.urls import path 
from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]
```

* Опишем процесс передачи управления проектом приложению ```posts```:
```
# project/urls.py
from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("posts.urls")),
]

```

### Шаг 8. Модульные тесты

* Сначала опишем тесты для модели:
```
from django.test import TestCase
from .models import Post 

# Create your tests here.

class PostModelTest(TestCase):
    def setUp(self):
        """
        Данный метод будет запускаться перед каждым тестом в данном классе
        """
        Post.objects.create(text="test text") # В виртуальной БД создадим 1-ый элемент в таблице Post

    def test_text_content(self):
        current_post = Post.objects.get(id=1) # Получаем пост с id = 1
        current_text = current_post.text  # текст в полученном посте
        expected_text = "test text" # что ожидаем увидеть
        self.assertEqual(current_text, expected_text)


```
* Запуск тестов через ```python manage.py test```

* Теперь напишем тесты для отображения:
```
class HomePageViewTest(TestCase):
    def test_view_by_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200) 

    def test_view_by_nickname(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200) 

    def test_view_with_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html") 

```