from django.test import TestCase
from django.urls import reverse # Функция, позволяющая получать url по никнейму
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

