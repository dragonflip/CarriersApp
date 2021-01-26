from django.forms import ModelForm, TextInput 
from .models import *


class BusForm(ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(BusForm, self).__init__(*args, **kwargs)
 
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-2'
            field.required = True
