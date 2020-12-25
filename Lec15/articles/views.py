#articles/views.py
from django.views.generic import ListView , DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy 
from .models import Article

from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "list_articles.html"
    context_object_name = "list_articles"
    login_url = 'login'


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article 
    template_name = "detail_article.html"
    context_object_name = "article"
    login_url = 'login'

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article 
    fields = ("title", "body")
    template_name = "update_article.html"
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Получаем автора СТАТЬИ и сравниваем его с ТЕКУЩИМ ПОЛЬЗОВАТЕЛЕМ, который 
        выполняет запрос
        """ 
        article = self.get_object()
        if article.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "delete_article.html"
    success_url = reverse_lazy("list_articles")
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Получаем автора СТАТЬИ и сравниваем его с ТЕКУЩИМ ПОЛЬЗОВАТЕЛЕМ, который 
        выполняет запрос
        """ 
        article = self.get_object()
        if article.author != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "new_article.html"
    fields = ('title', 'body')
    login_url = 'login' # Куда отправлять, если пользователь анонимный

    def form_valid(self, form):
        """
        Стандартный метод , который содержится в любом классе ....View
        Метод запускается при отправке любой формы
        """
        form.instance.author = self.request.user 
        """
        У формы в поле автора = занести пользователя, который эту форму заполнял
        """
        return super().form_valid(form)
    
