"""
Definition of urls for ForeignBerries.
"""

from django.urls import path, include, reverse_lazy
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app.forms import CustomSetPassword


urlpatterns = [
    path('authorization/', include(('app.urls', 'app'), namespace='authorization')),
    path('', include('admin-panel.urls')),
    path('admin/', admin.site.urls),

    # for password reset
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_new.html', 
        form_class=CustomSetPassword,
        success_url=reverse_lazy('authorization:password_reset_complete')), name='password_reset_confirm'),

    ]