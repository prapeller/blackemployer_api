from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from djangofront.forms import UserLoginForm, UserRegisterForm


@user_passes_test(lambda u: u is not None)
def index(request):
    context = {'title': 'Main'}
    return render(request, 'index.html', context)

@user_passes_test(lambda u: u is not None and u.is_active)
def verification(request):
    context = {'title': 'Verification'}
    return render(request, 'verification.html', context)


class LoginView(Login):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('djangofront:index')
    extra_context = {'title': 'Login'}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)


class LogoutView(Logout):
    next_page = reverse_lazy('djangofront:index')


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('djangofront:login')
    extra_context = {'title': 'Login'}
    success_message = "Your account was created successfully! Please verify your account by following link we sent to your email."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('djangofront:login'))
