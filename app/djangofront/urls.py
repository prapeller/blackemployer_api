from django.urls import path, include

from djangofront.views import index, LoginView, RegisterView, LogoutView

app_name = 'djangofront'

urlpatterns = [
    path('', index, name='index'),

    # users/login/ [name='login']
    # users/logout/ [name='logout']
    # users/password_change/ [name='password_change']
    # users/password_change/done/ [name='password_change_done']
    # users/password_reset/ [name='password_reset']
    # users/password_reset/done/ [name='password_reset_done']
    # users/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # users/reset/done/ [name='password_reset_complete']
    # path('', include('django.contrib.auth.urls')),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
