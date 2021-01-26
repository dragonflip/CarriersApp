from django.db import models
from datetime import datetime

class Bus(models.Model):
    company = models.CharField(max_length=60,null=True,blank=True)
    model = models.CharField(max_length=50,blank=False,default = '')
    yearOfIssue = models.PositiveIntegerField(max_length=10,blank=False,default = '')
    number = models.CharField(max_length=10,blank=False,default = '')
    VinNumber = models.CharField(max_length=10,blank=False,null=False,default = '')
    fuelConsumption = models.FloatField(max_length=10,blank=False,null=True,default = '')

    def __str__(self):
        return self.number

class Journey(models.Model):
    bus = models.ForeignKey(Bus,on_delete=models.CASCADE,blank=False,default = '')
    number = models.CharField(max_length=10,blank=False,default = '')
    fromWhere = models.CharField(max_length=60,blank=False,default = '')
    whereTo = models.CharField(max_length=60,blank=False,default = '')
    DepartureTime = models.TimeField(auto_now=False,blank=False,default = '')
    ArrivalTime = models.TimeField(auto_now=False,blank=False,default = '')
    FullDistance = models.FloatField(max_length=10,blank=False,default = '')

    def __str__(self):
        return self.number


class Station(models.Model):
    journey = models.ForeignKey(Journey,on_delete=models.CASCADE,blank=False,default = '')
    stationName = models.CharField(max_length=60,blank=False,default = '')
    distanceFromStart = models.FloatField(max_length=10,blank=False,default = '')
    stationArrivalTime = models.DateTimeField(auto_now=False,blank=False,default = '')
    stationDepartureTime = models.DateTimeField(auto_now=False,blank=False,default = '')

    def __str__(self):
        return self.stationName


class Ticket(models.Model):
    Types = (
        ('Дорослий', 'Normal'),
        ('Дитячий', 'Kids'),
        ('Пенсійний', 'Retiree'),
    )
    buyerName = models.CharField(max_length=50,blank=False,null=False,default = '')
    buyerSurname = models.CharField(max_length=50,blank=False,null=False,default = '')
    journey = models.ForeignKey(Journey,on_delete=models.CASCADE,blank=False,default = '')
    price = models.FloatField(max_length=10,blank=False,default = '')
    date = models.DateTimeField(auto_now=False, auto_now_add=False,blank=False,default = datetime.now())
    type = models.CharField(max_length=10, choices=Types,default = 'Normal')

    def __int__(self):
        return self.id
