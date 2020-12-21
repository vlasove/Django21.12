from django.http import HttpResponse, HttpRequest

# Создадим свое первое отображения.
# Все отображения(в виде функций) принимают один аргумент - request
def homePageView(request:HttpRequest):
    """
    Возвращает убогую гадость с надписью `Hello Web!`
    """
    return HttpResponse("<h1>Hello Web!</h1>")