from django.db import models
from django.urls import reverse

# данная функция отдает текущую пользовательскую модель
from django.contrib.auth import get_user_model

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_article', args=[str(self.id)])
