from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView,BlogDeleteView

urlpatterns = [
    path("post/<int:pk>/delete/", BlogDeleteView.as_view(), name = "delete_post"),
    path("post/<int:pk>/update/", BlogUpdateView.as_view(), name="update_post"),
    path("post/new/", BlogCreateView.as_view(), name = "new_post"),
    path("post/<int:pk>/", BlogDetailView.as_view(), name="detail_post"),
    path("", BlogListView.as_view(), name="home"),
]