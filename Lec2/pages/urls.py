from django.urls import path 
from .views import homePageView

# Название этого списка СТАНДАРТИЗИРОВАНО!!!!!
urlpatterns = [
    path("", homePageView)
]