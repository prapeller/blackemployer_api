from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as PasswordChange, AuthenticationForm
from django.contrib.auth.forms import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from companies.models import Company, Case, Comment


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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


class PasswordChangeForm(PasswordChange):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    first_name = forms.CharField(label='first_name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(label='last_name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    age = forms.IntegerField(label='age', widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'username', 'age')


class CompanyForm(forms.ModelForm):
    title = forms.CharField(label='title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    website = forms.URLField(label='website', widget=forms.URLInput(attrs={'class': 'form-control'}))
    image = forms.FileField(label='image', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Company
        fields = ('title', 'text', 'website', 'image')


class CompanyDetailForm(CompanyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class CaseForm(forms.ModelForm):
    case_date = forms.DateTimeField(label='date', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    case_description = forms.CharField(label='description', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    position = forms.CharField(label='position', widget=forms.TextInput(attrs={'class': 'form-control'}))
    position_description = forms.CharField(label='position description',
                                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))

    class Meta:
        model = Case
        fields = ('case_date', 'case_description', 'position', 'position_description')


class CaseDetailForm(CaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='text', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))
    image = forms.FileField(label='image', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Comment
        fields = ('text', 'image')


class TagForm(forms.Form):
    tag_title = forms.CharField(label='tag', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('tag_title',)


class ImageForm(forms.Form):
    image = forms.FileField(label='image', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        fields = ('image',)


