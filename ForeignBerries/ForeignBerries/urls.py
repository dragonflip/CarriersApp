"""
Definition of urls for ForeignBerries.
"""

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('authorization/', include(('app.urls', 'app'), namespace='authorization')),
    path('', include('admin-panel.urls')),
    path('admin/', admin.site.urls),
    ]