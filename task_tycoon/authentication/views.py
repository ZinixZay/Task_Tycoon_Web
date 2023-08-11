from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import NewUserForm, NewUserLoginForm

# Create your views here.


def logout_user(request):
    logout(request)
    return redirect('login')


class CreateUser(CreateView):
    form_class = NewUserForm
    template_name = 'authentication/registration.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {'title': 'Регистрация', **context}


class LoginUser(LoginView):
    form_class = NewUserLoginForm
    template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {'title': 'Вход', **context}

    def get_success_url(self):
        return reverse_lazy('home')
