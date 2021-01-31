from django.forms import ModelForm, TextInput 
from .models import *
from django import forms

class BusForm(ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(BusForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
            field.required = True

class TimeInput(forms.TimeInput):
    input_type = 'time'

class JourneyForm(ModelForm):
    class Meta:
        model = Journey
        fields = '__all__'

        widgets = {
        'DepartureTime': TimeInput(attrs={'class' : 'form-control'}),
        'ArrivalTime': TimeInput(attrs={'class' : 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(JourneyForm, self).__init__(*args, **kwargs)
 
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
            field.required = True

        self.fields['travelTime'].required = False


class StationForm(forms.ModelForm):
       class Meta:
           model = Station
           fields = '__all__'
           widgets = {
            'stationName' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Назва станції'}),
            'distanceFromStart' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Відстань від початку'}),
            'daysFromStart' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Днів', 'type' : 'number', 'min' : '0', 'style': 'width:80px'}),
            'hoursFromStart' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Годин','type' : 'number', 'min' : '0', 'max' : '23', 'style': 'width:100px'}),
            'minutesFromStart' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Хвилин', 'type' : 'number', 'min' : '0', 'max' : '59', 'style': 'width:100px'}),
            'stopTime' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Хвилин', 'type' : 'number', 'min' : '0', 'style': 'width:100px; margin: auto'}),
            #'stationArrivalTime' : TimeInput(attrs={'class' : 'form-control'}),
            #'stationDepartureTime' : TimeInput(attrs={'class' : 'form-control'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Введіть адресу зупинки'})

            }