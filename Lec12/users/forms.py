from .models import CustomUser

# Заготовки интерфейса пользовательской модели
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    """
    Наш интерфейс взаимодействия с нашей CustomUser моделью
    Создание юзера
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'age')# При создании пользователя еще хотим указывать
                                                        # и возраст



class CustomUserChangeForm(UserChangeForm):
    """
    Наш интерфейс взаимодействия с нашей CustomUser моделью
    Редактирование юзера
    """
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields =  ('username', 'email', 'age') #+ ('age', ) пока не будем редактировать возраст