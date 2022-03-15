from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import BaseDeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from djangofront.forms import UserLoginForm, UserRegisterForm, CompanyCreateForm
from companies.models import Company
from djangofront.mixin import UserIsNotNoneMixin, UserIsActiveMixin


@user_passes_test(lambda u: u is not None)
def index(request):
    context = {'title': 'Main'}
    return render(request, 'index.html', context)


@user_passes_test(lambda u: u is not None and u.is_active)
def verification(request):
    context = {'title': 'Verification'}
    return render(request, 'verification.html', context)


class LoginView(UserIsNotNoneMixin, Login):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('djangofront:index')
    extra_context = {'title': 'Login'}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)


class LogoutView(UserIsNotNoneMixin, LoginRequiredMixin, Logout):
    next_page = reverse_lazy('djangofront:index')


class RegisterView(UserIsNotNoneMixin, SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('djangofront:login')
    extra_context = {'title': 'Login'}
    success_message = "Your account was created successfully! Please verify your account by following the link we sent to your email."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy('djangofront:login'))


class CompanyList(UserIsActiveMixin, LoginRequiredMixin, ListView):
    model = Company
    extra_context = {'title': 'Companies List'}
    ordering = ['title']

    def get_queryset(self):
        return Company.objects.filter(is_active=True)


class UserCompanyList(UserIsActiveMixin, LoginRequiredMixin, ListView):
    model = Company
    extra_context = {'title': 'My Companies List'}
    ordering = ['title']

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user, is_active=True)


class CompanyCreate(UserIsActiveMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'companies/company_form.html'
    success_message = "You added new company!"

    def get_context_data(self, **kwargs):
        return {
            'form': CompanyCreateForm(instance=self.request.user),
        }


class CompanyUpdate(UpdateView):
    pass


class CompanyDelete(BaseDeleteView):
    pass


class CaseList(ListView):
    pass


class CaseCreate(CreateView):
    pass


class CaseUpdate(UpdateView):
    pass


class CaseDelete(BaseDeleteView):
    pass
