from django.urls import path
from django.contrib.auth import get_user_model
from .views import verify

app_name = 'users'

urlpatterns = [
    path('api/verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
