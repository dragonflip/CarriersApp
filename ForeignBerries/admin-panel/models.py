from django.db import models
from datetime import datetime, timedelta
import qrcode 
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class Bus(models.Model):
    company = models.CharField(max_length=60,null=True,blank=True)
    model = models.CharField(max_length=50,blank=False,default = '')
    yearOfIssue = models.PositiveIntegerField(blank=False,default = '')
    number = models.CharField(max_length=10,blank=False,default = '')
    VinNumber = models.CharField(max_length=10,blank=False,null=False,default = '')
    fuelConsumption = models.FloatField(max_length=10,blank=False,null=True,default = '')
    countOfSeats = models.PositiveIntegerField(blank=False,default = '')

    def __str__(self):
        return self.number

class Journey(models.Model):
    Days = (
        ('Крім неділі', 'Крім неділі'),
        ('По буднях', 'По буднях'),
    )

    bus = models.ForeignKey(Bus,on_delete=models.CASCADE,blank=False,default = '')
    number = models.CharField(max_length=10,blank=False,default = '')
    fromWhere = models.CharField(max_length=60,blank=False,default = '')
    whereTo = models.CharField(max_length=60,blank=False,default = '')
    DepartureTime = models.TimeField(auto_now=False,blank=False,default = '')
    travelTime = models.DurationField(blank=False,default = timedelta(days=0, hours=0, minutes = 0))
    DaysOfDeparture = models.CharField(max_length=20, choices=Days, default = 'Крім неділі')
    FullDistance = models.FloatField(max_length=10,blank=False,default = '')

    def __str__(self):
        return self.number


class Station(models.Model):
    journey = models.ForeignKey(Journey,on_delete=models.CASCADE,blank=False,default = '')
    stationName = models.CharField(max_length=60,blank=False,default = '')
    distanceFromStart = models.FloatField(max_length=10,blank=False,default = '')
    #travelTimeFromStart = models.DurationField(blank=False,default = timedelta(days=0, hours=0, minutes = 0))
    daysFromStart = models.IntegerField(blank=False)
    hoursFromStart = models.IntegerField(blank=False)
    minutesFromStart = models.IntegerField(blank=False)
    stopTime = models.IntegerField(blank=False)
    #stationArrivalTime = models.TimeField(auto_now=False,blank=False,default = '')
    #stationDepartureTime = models.TimeField(auto_now=False,blank=False,default = '')
    address = models.TextField(blank=False,default = '')
    
    def __str__(self):
        return str(self.id)

class Schedule(models.Model):
    journey_id = models.ForeignKey(Journey, related_name='journeys', on_delete=models.CASCADE)
    DepartureDate = models.DateField()
    ArrivalDate = models.DateField()
    DepartureTime = models.TimeField()
    ArrivalTime = models.TimeField()
    status = models.CharField(max_length=20, blank=False, default = 'Доступний')
    freeSeats  = models.PositiveIntegerField(blank=False,default = '')

    def __str__(self):
        return str(self.journey_id) + ' ' + str(self.DepartureDate)

class Ticket(models.Model):
    Types = (
        ('Дорослий', 'Дорослий'),
        ('Дитячий', 'Дитячий'),
    )
    user_id = models.IntegerField(blank=False,null=False,default = '')
    buyerName = models.CharField(max_length=50,blank=False,null=False,default = '')
    buyerSurname = models.CharField(max_length=50,blank=False,null=False,default = '')
    journey = models.ForeignKey(Journey,on_delete=models.CASCADE,blank=False,default = '')
    price = models.FloatField(max_length=10,blank=False,default = '')
    date = models.DateTimeField(auto_now=False, auto_now_add=False,blank=False, default = datetime.now())
    type = models.CharField(max_length=10, choices=Types,default = 'Normal')
    email = models.CharField(max_length=75,blank=False,null=False,default = '')
    phone = models.CharField(max_length=12,blank=False,null=False,default = '')
    fromWhere  = models.CharField(max_length=60,blank=False,default = '')
    whereTo = models.CharField(max_length=60,blank=False,default = '')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        tickets = Ticket.objects.all()
        if tickets.exists():
            last_ticket = Ticket.objects.all().latest('id')
            new_id = last_ticket.id + 1
        else:
           new_id = 1
        qrcode_img = qrcode.make(new_id)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{new_id}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
