from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import UserForm, AuthForm


User = get_user_model()


class LoginView(DjangoLoginView):
    template_name = 'login.html'
    form_class = AuthForm
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    template_name = ''


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    model = User
    form_class = UserForm
    success_message = '%(email)s cadastrado com sucesso'
    success_url = reverse_lazy('login')

