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
    # blank True => мы допускаем не назначение этого атрибута на уровне модели
    # - валидатор
