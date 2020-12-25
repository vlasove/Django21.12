#articles/views.py
from django.views.generic import ListView , DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy 
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "list_articles.html"
    context_object_name = "list_articles"


class ArticleDetailView(DetailView):
    model = Article 
    template_name = "detail_article.html"
    context_object_name = "article"

class ArticleUpdateView(UpdateView):
    model = Article 
    fields = ("title", "body")
    template_name = "update_article.html"

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "delete_article.html"
    success_url = reverse_lazy("list_articles")
    
