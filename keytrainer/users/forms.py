from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from bootstrap_app.forms import set_form_control
from .models import User


# TODO: Когда будут отзывы сделать подтверждение регистрации по почте, вроде есть уже готовая штука: https://django-registration.readthedocs.io/en/3.0/
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'placeholder': 'Подтверждение пароля'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_control(self.fields)


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_control(self.fields)


class UpdateUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('words_count', 'random_words')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_control(self.fields)