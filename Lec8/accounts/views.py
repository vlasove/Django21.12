from django.views.generic import CreateView
from django.urls import reverse_lazy
# Стандартный интерфейс взаимодействия со стандартным пользователем
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")
