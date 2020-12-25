## Лекция 15. Django Blog : P2

***Проблемы:***
* При создании поста можно выбрать в качестве автора ***ЛЮБОГО*** пользователя на нашем сервисе.
* Любой пользователь может зайти на наш сервис и начать создавать/удалять/обновлять информацию про существующие посты.
* Юзер может удалять/обновлять посты не собственного авторства.


### Шаг 1. Подстановка автора
Для того, чтобы в момент создания поста поле ```author``` подбиралось автоматически в зависиомсти от текущего залогиненного пользователя,  на уровне ```ArticleCreateView``` внесем следующие изменения.

```
class ArticleCreateView(CreateView):
    model = Article
    template_name = "new_article.html"
    fields = ('title', 'body')

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
    
```

### Шаг 2. LogrinRequired ссылки
Решили первую проблему (подстановка автора поста), но всплыла следующая - что если анонимный пользователь (не проходил login) попробует создать новый пост? Кого тогда будет подставлять модель?

В этой ситуации нас ждет ошибка, т.к. стандартный ```AnonymousUser``` не способен реализовать интерфейс ```CustomUser```.

В этой ситуации мы можем закрыться от анонимных пользователей ```LoginRequiredMixin```, который будет проверять :
* если пользователь прошел логин, то все ок, можно использовать отображения
* если пользователь анонимный - запрещаем прямой переход на данное отображение и перенаправляем пользователя на страницу с ```login```
```

from django.contrib.auth.mixins import LoginRequiredMixin


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
```

Закроем все остальные ```View``` связанные со статьями ```LoginRequiredMixin```. В итоге, ```articles/views.py``` теперь выглядит так:
```
#articles/views.py
from django.views.generic import ListView , DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy 
from .models import Article

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

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "delete_article.html"
    success_url = reverse_lazy("list_articles")
    login_url = 'login'
    

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
    
```

### Шаг 3. Запрет на взаимодействие
Для того, чтобы спровоцировать запрет на взаимодействие воспользуемся стандартным методом ```dispatch()```:
* если пользователь имеет отношение к объекту - все ок, dispatch() ничего не делает
* если пользователь не имеет отношения к объекту (но взаимодействует с ним) - dispatch() кидает исключение типа ```PermissionDenied```

Заходим в ```articles/views.py```:
````
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
```