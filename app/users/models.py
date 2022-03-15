import datetime
import hashlib
from random import random

from django.conf import settings
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse_lazy, reverse
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creates and returns a new user with Token"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        username = extra_fields.get('username')
        user.username = username if username else user.email
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and returns a new superuser with Token"""
        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Custom user model with unique username and email"""
    email = models.EmailField(max_length=64, unique=True,)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    username = models.CharField(max_length=64, unique=True, blank=True)
    age = models.PositiveIntegerField(null=True)
    activation_key = models.CharField(max_length=128, null=True, blank=True)
    activation_key_expiration_date = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def set_activation_key(self):
        salt = hashlib.sha1(str(random()).encode('utf8')).hexdigest()[:6]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()
        self.activation_key_expiration_date = timezone.now() + datetime.timedelta(hours=48)

    def activation_key_is_valid(self):
        return True if self.activation_key_expiration_date > timezone.now() else False

    def activate(self):
        self.is_active = True
        self.save()

    def send_verify_link(self):
        site = settings.DOMAIN_NAME
        verify_path = reverse('users:verify', args=[self.email, self.activation_key])
        varify_link = f'{site}{verify_path}'
        subject = f'{self.username}, activate your "blackemployer.com" account!'
        message = f'Please follow this link for that:\n{varify_link}'
        send_mail(subject, message, settings.EMAIL_HOST_USER,
                  [self.email], fail_silently=False)
        return varify_link


    # @receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance, created, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)
