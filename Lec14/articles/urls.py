# articles/urls.py
from django.urls import path 

from .views import ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path("<int:pk>/", ArticleDetailView.as_view(), name="detail_article"), # articles/3/
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name= "update_article"), # articles/2/update/
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name= "delete_article"), 
    path("", ArticleListView.as_view(), name="list_articles"), #
]