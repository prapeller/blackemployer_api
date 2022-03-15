from django.urls import path, include

from djangofront.views import (
    index, verification, LoginView, RegisterView, LogoutView,
    CompanyList, CompanyCreate, CompanyUpdate, CompanyDelete,
    CaseList, CaseCreate, CaseUpdate, CaseDelete,
)

app_name = 'djangofront'

urlpatterns = [

    # users/login/ [name='login']
    # users/logout/ [name='logout']
    # users/password_change/ [name='password_change']
    # users/password_change/done/ [name='password_change_done']
    # users/password_reset/ [name='password_reset']
    # users/password_reset/done/ [name='password_reset_done']
    # users/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # users/reset/done/ [name='password_reset_complete']
    # path('', include('django.contrib.auth.urls')),

    path('', index, name='index'),
    path('djangofront/verification/', verification, name='verification'),

    path('djangofront/register/', RegisterView.as_view(), name='register'),
    path('djangofront/login/', LoginView.as_view(), name='login'),
    path('djangofront/logout/', LogoutView.as_view(), name='logout'),

    path('djangofront/companies/', CompanyList.as_view(), name='company_list'),
    path('djangofront/companies/create/', CompanyCreate.as_view(), name='company_create'),
    path('djangofront/companies/update/', CompanyUpdate.as_view(), name='company_update'),
    path('djangofront/companies/delete/', CompanyDelete.as_view(), name='company_delete'),

    path('djangofront/cases/', CaseList.as_view(), name='case_list'),
    path('djangofront/cases/create/', CaseCreate.as_view(), name='case_create'),
    path('djangofront/cases/update/', CaseUpdate.as_view(), name='case_update'),
    path('djangofront/cases/delete/', CaseDelete.as_view(), name='case_delete'),

]
