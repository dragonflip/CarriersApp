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
        'DepartureTime': TimeInput(),
        'ArrivalTime': TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(JourneyForm, self).__init__(*args, **kwargs)
 
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
            field.required = True


class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = '__all__'