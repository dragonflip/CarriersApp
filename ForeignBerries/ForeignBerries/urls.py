"""
Definition of urls for ForeignBerries.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from app import forms, views
from app.views import VerificationView
from app.forms import CustomResetPassword, CustomSetPassword


urlpatterns = [
    path('', views.index, name='main'),
    path('login', views.login, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),

    path('search', views.search, name='search'),
    path('buy', views.buy, name='buy'),
    path('success', views.success, name='success'),

    path('admin/', admin.site.urls),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='app/password_reset.html', 
        #html_email_template_name= 'registration/password_reset_html_email.html',
        form_class=CustomResetPassword), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_new.html', form_class=CustomSetPassword), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
   ]
