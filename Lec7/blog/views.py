from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # выполняет редирект после отправки (после POST)
from .models import Post 
# Create your views here.

class BlogListView(ListView):
    model = Post 
    template_name = "home.html"
    context_object_name = "posts"

class BlogDetailView(DetailView):
    model = Post 
    template_name = "detail_post.html"
    context_object_name = "post"

class BlogCreateView(CreateView):
    model = Post 
    template_name = "new_post.html"
    fields = '__all__' # какие поля мы будем заполнять в веб-форме

class BlogUpdateView(UpdateView):
    model = Post 
    template_name = "update_post.html"
    fields = ['title', 'body'] # поля, которые я хочу обновлять

class BlogDeleteView(DeleteView):
    model = Post 
    template_name = "delete_post.html"
    success_url = reverse_lazy("home")