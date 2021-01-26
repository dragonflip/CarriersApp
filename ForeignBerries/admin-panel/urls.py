from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('busses/', views.busses, name = 'busses'),
    path('add_bus/', views.add_bus, name = 'add_bus'),
    path('update_bus/<str:bus_id>', views.update_bus, name = 'update_bus'),
    path('delete_bus/<str:bus_id>', views.delete_bus, name = 'delete_bus'),

    path('search', views.search, name='search'),
    path('buy', views.buy, name='buy'),
    path('success', views.success, name='success'),
    ]

