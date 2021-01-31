import datetime 
from datetime import date, datetime, timedelta, timezone, time
from django.shortcuts import render, redirect
from django.db.models.functions import Concat, Lower
from django.db.models import Sum, Q, Count, F, CharField, Value
from django.forms import inlineformset_factory
from .models import *
from .forms import *

def index(request):
    if request.user.groups.filter(name = 'admin').exists():
        update(request)

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

def add_journey(request):
    startAdr_query = request.POST.get('startAdr','')
    finalAdr_query = request.POST.get('finalAdr','')
    input_days = request.POST.get('d','')
    input_hours = request.POST.get('h','')
    input_minutes = request.POST.get('m','')


    form = JourneyForm()

    if request.method == 'POST':
        form = JourneyForm(request.POST)
        if form.is_valid():
            form.save()

            travel_time = timedelta(days= int(input_days), hours= int(input_hours), minutes = int(input_minutes))
            last_journey = Journey.objects.all().latest('id')
            last_journey_qs = Journey.objects.filter(id = last_journey.id)

            last_journey_qs.update(travelTime = travel_time)

            last_journey_values = last_journey_qs.values()
            for j in last_journey_values:
                fromWhere = j['fromWhere'] 
                whereTo = j['whereTo']
                DepartureTime = j['DepartureTime']
                travelTime = j['travelTime']
                FullDistance = j['FullDistance']

            newStation1 = Station(journey = last_journey, stationName = fromWhere, distanceFromStart = 0, 
                                  daysFromStart = 0, hoursFromStart = 0, 
                                  minutesFromStart = 0, stopTime = 0, address = startAdr_query)
            newStation1.save()

            newStation2 = Station(journey = last_journey, stationName = whereTo, 
                                  distanceFromStart = FullDistance, 
                                  daysFromStart = travelTime.days, hoursFromStart = travelTime.seconds//3600,
                                  minutesFromStart = (travelTime.seconds//60)%60, stopTime = 0,
                                  address = finalAdr_query)
            newStation2.save()

            return redirect('/')
    context = {'form' : form}
    return render(request, 'admin-panel/add-journey.html', context)


def update_journey(request, Journey_id):  
    journey = Journey.objects.get(id = Journey_id) 
    form = JourneyForm(instance=journey)
    input_days = request.POST.get('d','')
    input_hours = request.POST.get('h','')
    input_minutes = request.POST.get('m','')
    

    if request.method == 'POST':
        form = JourneyForm(request.POST, instance = journey)
        if form.is_valid():
            form.save()

            travel_time = timedelta(days= int(input_days), hours= int(input_hours), minutes = int(input_minutes))

            last_journey_qs = Journey.objects.filter(id__exact = journey.id)
            last_journey_qs.update(travelTime = travel_time)
            journeyNewValues = last_journey_qs.values()
            for j in journeyNewValues:
                fromWhere = j['fromWhere'] 
                whereTo = j['whereTo']
                DepartureTime = j['DepartureTime']
                ArrivalTime = j['ArrivalTime']
                FullDistance = j['FullDistance']

            station0 = Station.objects.filter(journey = journey).earliest('id')
            Station.objects.filter(journey = journey,id = station0.id).update( stationName = fromWhere, distanceFromStart = 0, stationArrivalTime = DepartureTime, stationDepartureTime = DepartureTime)
            station1 = Station.objects.filter(journey = journey,id = station0.id+1).update( stationName = whereTo, distanceFromStart = FullDistance, stationArrivalTime = ArrivalTime, stationDepartureTime = ArrivalTime)
            return redirect('journeys')

    context = {'form' : form, }
    return render(request, 'admin-panel/update-journey.html', context)


def delete_journey(request, Journey_id):
    journey = Journey.objects.get(id = Journey_id)

    if request.method == 'POST':
        journey.delete()
        return redirect('journeys')
    context = {'journey' : journey}
    return render(request, 'admin-panel/delete-journey.html', context)


def journeys(request):
    search_query = request.GET.get('search','')
    if request.method == 'GET':
        if search_query:
           journey = Journey.objects.annotate(pc = Concat(('id'),Value(' '),F('number'),Value(' '),F('bus__number'),Value(' '),('ArrivalTime'),Value(' '),F('DepartureTime'),Value(' '),F('FullDistance'), Value(' '),F('fromWhere'),Value(' '),F('whereTo'),output_field=CharField())).filter(pc__icontains=search_query)
        else:
            journey = Journey.objects.all()
    else: 
        journey = Journey.objects.all()

    return render(request, 'admin-panel/journeys.html', {'journey' : journey})


def journey_stations(request, Journey_id):
    StationFormSet = inlineformset_factory(Journey, Station, form = StationForm, extra = 1)
    journey = Journey.objects.get(id = Journey_id)
    formset = StationFormSet(instance = journey)
    if request.method == 'POST':
        formset = StationFormSet(request.POST, instance = journey)
        if formset.is_valid():
            formset.save()
            return redirect('/journey_stations/' + Journey_id + '/')
    context = {'formset' : formset}
    return render(request, 'admin-panel/journey-stations.html', context)


def tickets(request):
    search_query = request.GET.get('search','')
    if request.method == 'GET':
        if search_query:
           tickets = Ticket.objects.annotate(pc = Concat(('buyerName'), Value(' '),('buyerSurname'), Value(' '),F('price'), Value(' '),F('date'), Value(' '),F('journey__number'), Value(' '),F('type'),output_field=CharField())).filter(pc__icontains=search_query)
        else:
            tickets = Ticket.objects.all()
    else: 
        tickets = Ticket.objects.all()
    
    context = {'tickets' : tickets}
    return render(request, 'admin-panel/tickets.html', context)


def statistics(request):
    dat = request.POST.get('valu', '')
    datan = request.POST.get('validol', '')
    jrns = Journey.objects.all()
    js = 'не обрано'
    total_sold = 0
    if request.method == 'POST':
        jrnsbus = request.POST.get('jrns', '')
        js = jrnsbus
        if jrnsbus == 'не обрано':
            total_tickets = 0
            total_jrns = 0
            total_tickets_N = 0
            total_tickets_K = 0

        elif dat and datan and jrnsbus != 'None':
            total_sold = (Ticket.objects.filter(journey = Journey.objects.get(number=jrnsbus)).filter(Q(date__gte = dat) & Q(date__lte = datan)).aggregate(total_sold=Sum('price')))
            total_tickets = (Ticket.objects.filter(journey = Journey.objects.get(number=jrnsbus)).filter(Q(date__gte = dat) & Q(date__lte = datan)).count())
            total_tickets_N = (Ticket.objects.filter(journey = Journey.objects.get(number=jrnsbus)).filter(Q(date__gte = dat) & Q(date__lte = datan)).filter(type = 'Дорослий').count())
            total_tickets_K = (Ticket.objects.filter(journey = Journey.objects.get(number=jrnsbus)).filter(Q(date__gte = dat) & Q(date__lte = datan)).filter(type = 'Дитячий').count())
            datetime_object = datetime.strptime(dat, '%Y-%m-%d')  
            datetime_object = datetime.strptime(dat, '%Y-%m-%d')  
            total_jrns = (Schedule.objects.filter(journey_id = Journey.objects.get(number=jrnsbus)).filter(Q(DepartureDate__gte = dat) & Q(DepartureDate__lte = datan)).count())
            
        elif dat and datan and jrnsbus == 'None':
            total_tickets = (Ticket.objects.filter(Q(date__gte = dat) & Q(date__lte = datan)).count())
            total_sold = (Ticket.objects.filter(Q(date__gte = dat) & Q(date__lte = datan)).aggregate(total_sold=Sum('price')))
            total_tickets_N = (Ticket.objects.filter(Q(date__gte = dat) & Q(date__lte = datan)).filter(type = 'Дорослий').count())
            total_tickets_K = (Ticket.objects.filter(Q(date__gte = dat) & Q(date__lte = datan)).filter(type = 'Дитячий').count())
            datetime_object = datetime.strptime(dat, '%Y-%m-%d')  
            datetime_object = datetime.strptime(dat, '%Y-%m-%d') 
            total_jrns = (Schedule.objects.filter(Q(DepartureDate__gte = dat) & Q(DepartureDate__lte = datan)).count())   
            
        else:
            total_sold = 0
            total_tickets = 0
            total_jrns = 0
            total_tickets_N = 0
            total_tickets_K = 0
    else :
        total_sold = 0
        total_tickets = 0
        total_jrns = 0
        total_tickets_N = 0
        total_tickets_K = 0

    if total_sold != 0:
        total_sold = total_sold['total_sold']

        if total_sold == None:
            total_sold = 0

    context = {'total_sold' : total_sold,  'jrns' : jrns, 'dat' : dat, 'datan' : datan, 'js' : js, 'total_tickets' : total_tickets, 'total_jrns' : total_jrns, 'total_tickets_N' : total_tickets_N, 'total_tickets_K' : total_tickets_K}
    return render(request, 'admin-panel/statistics.html', context)

def schedule(request):
    journeys = Journey.objects.all()
    context = { 'journeys' : journeys }
    return render(request, 'admin-panel/schedule.html', context)

def update(request):
    date_now = date.today()
    last_day = date_now + timedelta(days=7)

    delta = timedelta(days=1)

    Schedule.objects.filter(DepartureDate__lt = date_now).delete()

    all_journeys = Journey.objects.all()

    for journey in all_journeys:
        while date_now <= last_day:
            dates = Schedule.objects.filter(journey_id = journey, DepartureDate = date_now)

            if not dates.exists():
                time = journey.DepartureTime
                weekday = date_now.weekday() 
                departure_datetime = datetime.combine(date_now, time)
                arrival_datetime = departure_datetime + journey.travelTime
                arrival_date = arrival_datetime.date()
                arrival_time = arrival_datetime.time()

                if journey.DaysOfDeparture.lower() == 'по буднях' and weekday != 5 and weekday != 6:
                    bus = journey.bus
                    newObj = Schedule(journey_id = journey, DepartureDate = date_now, DepartureTime = time, ArrivalDate = arrival_date, ArrivalTime = arrival_time, freeSeats = bus.countOfSeats)
                    newObj.save()

                if journey.DaysOfDeparture.lower() == 'крім неділі' and weekday != 6:
                    bus = journey.bus
                    newObj = Schedule(journey_id = journey, DepartureDate = date_now, DepartureTime = time, ArrivalDate = arrival_date, ArrivalTime = arrival_time, freeSeats = bus.countOfSeats)
                    newObj.save()
            date_now += delta
        date_now = date.today()

def search(request):
    fromWhere_query = request.GET.get('fromWhere','')
    whereTo_query = request.GET.get('whereTo','')
    date_query = request.GET.get('date','')

    journeys = []
    stations_fromWhere1 = []
    stations_whereTo1 = []
    schedule = []
    dates = []

    journeys1 = Journey.objects.all()

    for j in journeys1:
        stations_fromWhere = Station.objects.filter(journey = j, stationName__iexact = fromWhere_query)
        distance1_value = stations_fromWhere.values()

        stations_whereTo = Station.objects.filter(journey = j, stationName__iexact = whereTo_query)
        distance2_value = stations_whereTo.values()
        
        schedule_date = Schedule.objects.filter(journey_id = j, DepartureDate = date_query)

        if distance1_value.exists() and distance2_value.exists():
            for station1 in distance1_value:
                distance1 = station1['distanceFromStart'] 
                days1 = station1['daysFromStart'] 
                hours1 = station1['hoursFromStart'] 
                minutes1 = station1['minutesFromStart'] 
                stop1 = station1['stopTime'] 

            for station2 in distance2_value:
                distance2 = station2['distanceFromStart']
                days2 = station2['daysFromStart'] 
                hours2 = station2['hoursFromStart'] 
                minutes2 = station2['minutesFromStart'] 

            travel_time1 = timedelta(days=days1, hours=hours1, minutes=minutes1+stop1)
            travel_time2 = timedelta(days=days2, hours=hours2, minutes=minutes2)

            if distance1 < distance2 and schedule_date.exists():

                schedule_date = Schedule.objects.get(journey_id = j, DepartureDate = date_query)
                departure_datetime = datetime.combine(schedule_date.DepartureDate, schedule_date.DepartureTime)

                departure = departure_datetime + travel_time1
                arrival = departure_datetime + travel_time2

                journeys += Journey.objects.annotate(price = F('FullDistance') * 0 +(distance2-distance1)).filter(id__contains = j.id)
                stations_fromWhere1 += stations_fromWhere
                stations_whereTo1 += stations_whereTo
                schedule += Schedule.objects.filter(journey_id = j, DepartureDate = date_query)

                dates.append({'journey' : j, 'departure' : departure, 'arrival' : arrival})
    context = {'journeys' : journeys, 
               'st_fromWhere' : stations_fromWhere1, 
               'st_whereTo' : stations_whereTo1, 
               'fromWhere' :  fromWhere_query,
               'whereTo' :  whereTo_query, 
               'schedule' : schedule,
               'date_journey' : date_query,
               'dates' : dates }
    return render(request, 'app/search.html', context)

def buy(request, id,price,fromWhere,whereTo, date_journey):
    journey = Journey.objects.filter(id__exact = id)[0]
    FrowWhere = Station.objects.filter(journey = journey,stationName = fromWhere)[0]
    WhereTo = Station.objects.filter(journey = journey,stationName = whereTo)[0]
    schedule = Schedule.objects.filter(journey_id = journey).earliest('id')


    context = {'id':id, 
               'full_price' : int(float(price)), 
               'kids_price' : int(float(price) * 0.75),
               'journey' : journey,
               'FromWhere': FrowWhere,
               'WhereTo':WhereTo,
               'schedule':schedule,
               'date_journey' : date_journey }
    return render(request, 'app/buy.html',context)

def success(request, id, price, fromWhere, whereTo, date_journey):
    journey = Journey.objects.filter(id__exact = id)[0]
    buyerName_query = request.GET.get('buyerName','')
    buyerSurname_query = request.GET.get('buyerSurname','')
    email_query = request.GET.get('email','')
    phone_query = request.GET.get('phone','')
    type = request.GET.get('type','')

    if(type == 'Дитячий'):
        price = int(float(price) * 0.75)
    else:
        type = 'Дорослий'

    id = 0
    if request.user.is_authenticated:
        id = request.user.id

    newObj = Ticket(user_id = id, buyerName = buyerName_query, buyerSurname = buyerSurname_query, journey = journey, price = price, date = datetime.now(), type = type ,email = email_query, phone = phone_query, fromWhere = fromWhere, whereTo = whereTo)
    newObj.save()

    schedule_obj = Schedule.objects.get(journey_id = journey, DepartureDate = date_journey)
    Schedule.objects.filter(journey_id = journey, DepartureDate = date_journey).update(freeSeats = schedule_obj.freeSeats-1)


    context = {'ticket': newObj }
    return render(request, 'app/success.html', context)

def my_tickets(request):
    tickets_qs = Ticket.objects.filter(user_id = request.user.id)
    context = { 'tickets' : tickets_qs }
    return render(request, 'admin-panel/my-tickets.html', context)
