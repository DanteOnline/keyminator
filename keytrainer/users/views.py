from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib import auth, messages
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from .models import User
from .forms import UserRegistrationForm, UserAuthenticationForm, UpdateUserForm


class LoginFormView(SuccessMessageMixin, FormView):
    form_class = UserAuthenticationForm
    template_name = 'users/auth.html'
    success_url = '/'
    success_message = 'Добро пожаловать'


    def form_valid(self, form):
        current_user = form.get_user()
        auth.login(self.request, current_user)
        return super().form_valid(form)


def logout(request):
    # TODO: В шаблоне через форму едет верстка, сделать метод пост и переделать верстку
    # if request.method == 'POST':
    #     auth.logout(request)
    #     return HttpResponseRedirect(reverse('users:login'))
    # else:
    #     raise Http404
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Пока')
    return HttpResponseRedirect(reverse('users:login'))


# Попробуем через createview сделать регистрацию
class UserCreateView(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались'
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('main:office'))
    else:
        edit_form = UpdateUserForm(instance=request.user)

    content = {'form': edit_form}

    return render(request, 'users/edit.html', content)