#articles/views.py
from django.views.generic import ListView 
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = "list_articles.html"
    context_object_name = "list_articles"
