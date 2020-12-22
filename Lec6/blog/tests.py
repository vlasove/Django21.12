from django.test import TestCase
from django.urls import reverse
from .models import Post 
from django.contrib.auth import get_user_model # Функция, возвращающая
                                               # модель текущего пользователя

# Create your tests here.

class BlogTests(TestCase):
    def setUp(self):
        """
        Данный метод выполняется каждый раз заново перд каждым тестом
        Внутри этого методы мы хотим в нашей виртуальной БД определить
        * пользоватея
        * какой-нибудь пост, созданыый этим пользователем
        """
        self.user = get_user_model().objects.create_user(
            username = "testuser",
            email="test@testmail.com",
            password="testpassword",
        ) 

        self.post = Post.objects.create(
            title = "Post test title",
            body = "Post test body",
            author = self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.post),  "Post test title")

    def test_post_right_content(self):
        self.assertEqual(str(self.post.title), "Post test title")
        self.assertEqual(str(self.post.body), "Post test body")
        self.assertEqual(str(self.post.author), "testuser")

    def test_post_list_view_by_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Post test body")

    def test_post_list_view_by_nickname(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertContains(response, "Post test body")

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000000/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

        self.assertTemplateUsed(response, "detail_post.html")
        self.assertContains(response, "Post test title")

