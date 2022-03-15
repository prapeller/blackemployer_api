from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from companies.models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label='name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Company
        fields = ('name',)


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Enter your password'}),
    )

    error_messages = {
        "invalid_login": _("Please enter a correct %(email)s and password. Note that both fields may be case-sensitive."),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = get_user_model().objects.get(email=email)
            except (Exception, ObjectDoesNotExist) as e:
                print(e)
                raise ValidationError(self.error_messages["inactive"], code="inactive", )

            if user:
                self.confirm_login_allowed(user)

            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(self.error_messages["inactive"], code="inactive", )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"email": self.email},
        )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password1 = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Enter your password'}),
    )
    password2 = forms.CharField(
        label='confirm',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'class': 'form-control', 'placeholder': 'Confirm your password'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = get_user_model().objects.create_user(email=self.cleaned_data["email"], password=self.cleaned_data["password1"])
        user.set_activation_key()
        user.send_verify_link()
        user.save()
        return user


class CompanyCreateForm(forms.ModelForm):
    title = forms.CharField(label='name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='name', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    image = forms.FileField(label='image', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Company
        fields = ('title', 'text', 'image')