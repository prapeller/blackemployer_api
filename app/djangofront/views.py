from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as Login, LogoutView as Logout, PasswordChangeView as PasswordChange
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import BaseDeleteView, ProcessFormView, BaseFormView

from companies.models import Company, Case
from content.models import Tag
from djangofront.forms import (UserLoginForm, UserRegisterForm, UserProfileForm,
                               CompanyForm, CaseForm, ImageForm, TagForm, PasswordChangeForm, CompanyDetailForm)
from djangofront.mixin import UserIsNotNoneMixin, UserIsActiveMixin, UserIsSuperuserMixin, PreviousPageMixin


@user_passes_test(lambda u: u is not None)
def index(request):
    context = {"title": "Main"}
    return render(request, "index.html", context)


@user_passes_test(lambda u: u is not None and u.is_active)
def verification(request):
    context = {"title": "Verification"}
    return render(request, "verification.html", context)


class LoginView(PreviousPageMixin, UserIsNotNoneMixin, Login):
    form_class = UserLoginForm
    template_name = "login.html"
    success_url = reverse_lazy("djangofront:index")
    extra_context = {"title": "Login"}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)


class ProfileView(PreviousPageMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = "profile.html"
    success_message = "Your profile was updated successfully!"

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy("djangofront:profile", kwargs={"pk": self.object.pk})
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, Logout):
    next_page = reverse_lazy("djangofront:index")


class RegisterView(PreviousPageMixin, SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("djangofront:login")
    extra_context = {"title": "Login"}
    success_message = "Your account was created successfully! Please verify your account by following the link we sent to your email."

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(reverse_lazy("djangofront:login"))


class PasswordChangeView(PreviousPageMixin, PasswordChange):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("djangofront:index")
    template_name = "password_change.html"


class CompanyList(PreviousPageMixin, LoginRequiredMixin, ListView):
    model = Company
    extra_context = {"title": "blackemployer companies list"}
    ordering = ["title"]

    def get_queryset(self):
        return Company.objects.filter(is_active=True)


class UserCompanyList(PreviousPageMixin, LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies/company_list_user.html'
    extra_context = {"title": "blackemployer my companies list"}
    ordering = ["title"]

    def get_queryset(self):
        return Company.objects.filter(creator=self.request.user, is_active=True)


class CompanyCreate(PreviousPageMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "companies/company_form.html"
    success_message = "Success! New company is created!"
    extra_context = {
        "title": "blackemployer - company create"
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.success_url = reverse_lazy("djangofront:company_update", kwargs={"pk": self.object.pk})
        return super().form_valid(form)


class CompanyDetail(PreviousPageMixin, LoginRequiredMixin, UpdateView):
    model = Company
    template_name = "companies/company_detail.html"
    form_class = CompanyDetailForm
    extra_context = {
        "title": "blackemployer - company detail",
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({"sub_object_list": Case.objects.filter(company=self.object)})
        return super().get(request, *args, **kwargs)


class CompanyUpdate(PreviousPageMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    template_name = "companies/company_form.html"
    form_class = CompanyForm
    extra_context = {
        "title": "blackemployer - company update"
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({"sub_object_list": Case.objects.filter(company=self.object)})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy("djangofront:company_update", kwargs={"pk": self.object.pk})
        return super().form_valid(form)


class CompanyDelete(BaseDeleteView):
    model = Company

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.success_url = reverse_lazy("djangofront:company_list")
        return HttpResponseRedirect(self.success_url)


class CaseList(LoginRequiredMixin, ListView):
    pass


class CaseCreate(PreviousPageMixin, UserIsActiveMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    def get(self, request, *args, **kwargs):
        from_url_str = request.META.get('HTTP_REFERER')
        if '/companies/update/' in from_url_str:
            company_id = int(from_url_str.split('/')[-2])
            self.object = Case.objects.create(
                company=Company.objects.get(id=company_id),
                creator=request.user
            )
        return HttpResponseRedirect(reverse_lazy('djangofront:case_update', kwargs={'pk': self.object.pk}))


class CaseDetail(PreviousPageMixin, DetailView):
    pass


class CaseUpdate(PreviousPageMixin, UpdateView):
    model = Case
    form_class = CaseForm
    extra_context = {
        'title': 'blackemployer - case',
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.extra_context.update({
            'comment_list': self.object.comments,
            'tags_list': self.object.tags.all(),
            'image_form': ImageForm(),
            'tag_form': TagForm(),
        })
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('djangofront:case_update', kwargs={'pk': self.object.pk})
        return super().form_valid(form)


class CaseDelete(BaseDeleteView):
    model = Case

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = reverse_lazy("djangofront:company_update", kwargs={"pk": self.object.company.pk})
        return super().delete(self, request, *args, **kwargs)
















class UserCaseList(UserIsActiveMixin, LoginRequiredMixin, ListView):
    model = Case
    extra_context = {"title": "My Case List"}
    ordering = ["updated_at"]

    def get_queryset(self):
        return Case.objects.filter(creator=self.request.user, is_active=True)


def update_case_with_ajax(request, pk):
    case = Case.objects.get(pk=pk)

    delete_tag_pk = request.GET.get('delete_tag_pk')
    if delete_tag_pk:
        tag_pk = int(delete_tag_pk)
        tag = Tag.objects.get(pk=tag_pk)
        case_tags = case.tags.filter(case_tags__tags__in=tag)
        case_tags.delete()

    add_tag_title = request.POST.get('add_tag_title')
    if add_tag_title:
        tag_title = add_tag_title
        tag, is_created = Tag.objects.get_or_create(title=tag_title)
        case.tags.add(tag)

    context = {
        'tags_list': case.tags.all(),
    }
    tags_html = render_to_string('companies/includes/tags.html', context, request)

    return JsonResponse({
        'tags_html': tags_html,
    })


def search_elems_with_ajax(request):
    search_str = request.GET.get('search_str')
    companies_list = []
    cases_list = []
    if search_str:
        companies_list = Company.objects.filter(
            Q(title__icontains=search_str) | Q(slug__icontains=search_str) | Q(website__icontains=search_str) | Q(
                text__icontains=search_str)
        )
        cases_list = Case.objects.filter(
            Q(case_description__icontains=search_str) | Q(position__icontains=search_str) | Q(position_description__icontains=search_str)
        )

    context = {
        'companies_list': companies_list,
        'cases_list': cases_list,
    }
    companies_list_html = render_to_string('companies/includes/search_companies.html', context, request)
    cases_list_html = render_to_string('companies/includes/search_cases.html', context, request)
    return JsonResponse({
        'companies_list_html': companies_list_html,
        'cases_list_html': cases_list_html,
    })


