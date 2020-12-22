from django.shortcuts import render
# Стандартный шаблон-отображение статической страницы
from django.views.generic import TemplateView 

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"
