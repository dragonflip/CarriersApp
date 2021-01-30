from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('busses/', views.busses, name = 'busses'),
    path('add_bus/', views.add_bus, name = 'add_bus'),
    path('update_bus/<str:bus_id>', views.update_bus, name = 'update_bus'),
    path('delete_bus/<str:bus_id>', views.delete_bus, name = 'delete_bus'),


    path('journeys/', views.journeys, name = 'journeys'),
    path('add_journey/', views.add_journey, name = 'add_journey'),
    path('update_journey/<str:Journey_id>', views.update_journey, name = 'update_journey'),
    path('delete_journey/<str:Journey_id>', views.delete_journey, name = 'delete_journey'),
    path('journey_stations/<str:Journey_id>/', views.journey_stations, name = 'journey_stations'),

    path('tickets/', views.tickets, name = 'tickets'),

    path('statistics/', views.statistics, name = 'statistics'),

    path('schedule/', views.schedule, name = 'schedule'),

    path('search', views.search, name='search'),
    path('buy/<str:id>&<str:price>', views.buy, name='buy'),
    path('success', views.success, name='success'),
    ]

