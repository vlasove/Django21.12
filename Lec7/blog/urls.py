from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView

urlpatterns = [
    path("post/new/", BlogCreateView.as_view(), name = "new_post"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="detail_post"),
    path("", BlogListView.as_view(), name="home"),
]