## Лекция 9. Создание собственной модели пользователя

***Проблема:*** в стандартном ```auth.User``` присуствует много чего интересного, но атрибутов и методов данной модели зачастую (98% случаев) недостаточно.

***Рещение:*** создадим собственную модель пользователя и "подложим" ее в наш проект вместо уже существующего.

### Шаг 1. Инициализация проекта.
* ```pipenv shell```
* ```pipenv install django```
* ```django-admin startproject project .```
* ```python manage.py startapp users``` - мое приложение для работы с пользователем

***ВАЖНО****: не выполнять запуска сервера и первичной миграции до тех пор, пока не будет совершена подмена пользователя.

* Зарегестрируем приложение для прокекта: ```settings.py -> INSTALLED_APPS..```
* В ```settings.py``` в самом низу укажем, какая теперь пользовательская модель будет использоваться. (Назовем свою модель ```CustomUser```).
```
....
# Подмена пользовательской модели
AUTH_USER_MODEL = 'users.CustomUser'
```

### Шаг 2. Создание пользовательской модели
* Заходим в ```users/models.py```
* Создаем свою пользовательскую модель на основе ****НИЗКОУРОВНЕВОЙ СУЩНОСТИ ЮЗЕРА*** - ```AbstractUser```
* Добавим пользователю поле - возраст (мы знаем, что в стандартном юзере возраста нет!)
```
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    """
    Определим поле age
    """
    age = models.PositiveIntegerField(null=True, blank=True)
    # PositiveIntegerFiled = > Unsigned Int
    # null True=> что мы допускаем NULL значение в таблицах - отпечаток в бд
    # blank True => мы допускаем не назначение этого атрибута на уровне модели - валидатор

```

* Пропишем формы взаимодействия (интерфейс) модели ```users/forms.py``` (нам нужен способ создания нового юзера и способ редактирвоания информации у существующего)
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
        fields = UserCreationForm.Meta.fields + ('age',) # При создании пользователя еще хотим указывать
                                                        # и возраст



class CustomUserChangeForm(UserChangeForm):
    """
    Наш интерфейс взаимодействия с нашей CustomUser моделью
    Редактирование юзера
    """
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields 
```

* Теперь необходимо данные интерфейсы привязать к панели администратора (чтобы можно было жмакать на плюсик и создавать нового пользователя, и на карандашик - чтобы редактировать существуюшего пользователя). Заходим в ```users/admin.py```:
```
from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Низкоуровневый админский интерфейс
from django.contrib.auth.admin import UserAdmin 
# Register your models here.


# Создаем свой интерфейс по взаимодействию с моделью на основе UserAdmin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser


# Регистрируем интерфейс в панель
admin.site.register(CustomUser, CustomUserAdmin)

```

* Теперь выполняем подготовку миграций:
```python manage.py makemigrations users```
* И выполним полную первичную миграцию для всего проекта:
```python manage.py migrate```

### Шаг 3. Создадим суперпользователя
* ```python manage.py createsuperuser```
* ```python manage.py runserver```
* Перейдем в ```admin/```
* Подскажем, какие колонки отображать в интерефейсе администратора (в панели администратора):
```
# users/admin.py
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "age", "username", "is_staff"]
```