from django.urls import path
from .views import UserCreateView, logout, LoginFormView, edit

app_name = 'users'

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('logout/', logout, name='logout'),
    path('update/', edit, name='update'),
]
