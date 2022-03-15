from django.contrib import auth
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserModelSerializer


def verify(request, email: str, activation_key: str):
    try:
        user = get_user_model().objects.get(email=email)
        if user and user.activation_key == activation_key and user.activation_key_is_valid():
            user.activation_key = ''
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse_lazy('djangofront:verification'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse_lazy('djangofront:index'))


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
