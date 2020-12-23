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