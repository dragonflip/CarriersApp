from django.shortcuts import render, redirect
from django.db.models.functions import Concat, Lower
from django.db.models import Sum, Q, Count, F, CharField, Value
from .models import *
from .forms import *

def index(request):
    return render(request, 'app/index.html')

def busses(request):
    search_query = request.GET.get('search','')
    if request.method == 'GET':
        if search_query:
           buses = Bus.objects.annotate(pc = Concat(('company'), Value(' '),('model'), Value(' '),F('yearOfIssue'), Value(' '),F('number'), Value(' '),F('VinNumber'), Value(' '),F('fuelConsumption'),output_field=CharField())).filter(pc__icontains=search_query)
        else:
            buses = Bus.objects.all()
    else: 
        buses = Bus.objects.all()
    
    context = {'buses' : buses}
    return render(request, 'admin-panel/busses.html', context)

def add_bus(request):
    form  = BusForm()

    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('busses')

    context = {'form' : form}
    return render(request, 'admin-panel/add-bus.html', context)

def update_bus(request, bus_id):
    bus = Bus.objects.get(id = bus_id)
    form = BusForm(instance=bus)

    if request.method == 'POST':
        form = BusForm(request.POST, instance = bus)
        if form.is_valid():
            form.save()
            return redirect('/busses')

    context = {'form' : form}
    return render(request, 'admin-panel/add-bus.html', context)


def delete_bus(request, bus_id):
    bus = Bus.objects.get(id = bus_id)
    if request.method == "POST":
        bus.delete()
        return redirect('/busses')
    context = {'bus' : bus}
    return render(request, 'admin-panel/delete-bus.html', context) 

