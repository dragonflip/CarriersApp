from django.db import models

class Bus(models.Model):
    company = models.CharField(max_length=60,null=True,blank=True)
    model = models.CharField(max_length=50,blank=False,default = '')
    yearOfIssue = models.PositiveIntegerField(max_length=10,blank=False,default = '')
    number = models.CharField(max_length=10,blank=False,default = '')
    VinNumber = models.CharField(max_length=10,blank=False,null=False,default = "")
    fuelConsumption = models.FloatField(max_length=10,blank=False,null=True,default = '')

    def __str__(self):
        return self.number
