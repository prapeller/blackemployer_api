from django.urls import path, include

from djangofront.views import (
    index, verification, LoginView, RegisterView, PasswordChangeView, LogoutView, ProfileView,
    CompanyList, CompanyCreate, CompanyUpdate, CompanyDetail, CompanyDelete,
    CaseList, CaseCreate, CaseDetail, CaseUpdate, CaseDelete,
    UserCaseList, UserCompanyList,
    update_case_with_ajax, search_elems_with_ajax
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
    # path('djangofront/profile/', include('django.contrib.auth.urls')),

    path('', index, name='index'),
    path('djangofront/verification/', verification, name='verification'),
    path('djangofront/search_elems_with_ajax/', search_elems_with_ajax, name='search_elems_with_ajax'),

    path('djangofront/register/', RegisterView.as_view(), name='register'),
    path('djangofront/login/', LoginView.as_view(), name='login'),
    path('djangofront/logout/', LogoutView.as_view(), name='logout'),
    path('djangofront/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('djangofront/profile/password_change/', PasswordChangeView.as_view(), name='password_change'),

    path('djangofront/companies/', CompanyList.as_view(), name='company_list'),
    path('djangofront/companies/create/', CompanyCreate.as_view(), name='company_create'),
    path('djangofront/companies/update/<int:pk>/', CompanyUpdate.as_view(), name='company_update'),
    path('djangofront/companies/detail/<int:pk>/', CompanyDetail.as_view(), name='company_detail'),
    path('djangofront/companies/delete/<int:pk>/', CompanyDelete.as_view(), name='company_delete'),

    path('djangofront/cases/', CaseList.as_view(), name='case_list'),
    path('djangofront/cases/create/', CaseCreate.as_view(), name='case_create'),
    path('djangofront/cases/update/<int:pk>/', CaseUpdate.as_view(), name='case_update'),
    path('djangofront/cases/detail/<int:pk>/', CaseDetail.as_view(), name='case_detail'),
    path('djangofront/cases/delete/<int:pk>/', CaseDelete.as_view(), name='case_delete'),

    path('djangofront/cases/update_case_with_ajax/<int:pk>/', update_case_with_ajax, name='update_case_with_ajax'),

    path('djangofront/usercompanies/', UserCompanyList.as_view(), name='user_company_list'),
    path('djangofront/usercases/', UserCaseList.as_view(), name='user_case_list'),
]
