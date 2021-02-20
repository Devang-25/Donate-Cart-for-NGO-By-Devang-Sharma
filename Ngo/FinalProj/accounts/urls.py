from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ngo/register/',views.ngo_register,name='ngo_register'),
    path('accountcreate/',views.accountcreate,name='accountcreate'),
    path('ngodetail/',views.ngodetail,name='ngodetail'),
    path('create/', views.edit_view_add, name='edit_view_add'),
    path('delete/',views.delete_view, name='delete_view'),
    path('edit/',views.edit_view, name='edit_view'),
    path('donate/',views.donator_view,name='donator'),
    path('donate/<phone>/',views.donation_confirm,name='don_confirm'),
    path('change-password/', views.MyPasswordChangeView.as_view(), name='reset'),
    path('ngodetail/donators/', views.donators, name='donators'),
    path('donater/signup/',views.d_signup,name='d_signup'),
    path('donators/', views.donators, name='donators'),
    path('contact/',views.contactus, name='contact')
    ]
