from django import forms
from datetime import datetime
from bootstrap_datepicker_plus.widgets import DatePickerInput

from django.forms import ModelForm, NumberInput
from django.core.exceptions import ValidationError
from .models import CategoriaHabitacion, Habitacion, Reserva

class CatHabitacionForm(ModelForm):
    class Meta:
        model = CategoriaHabitacion
        fields = '__all__'

class HabitacionForm(ModelForm):
    class Meta:
        model = Habitacion
        fields = '__all__'

class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
       # fields = '__all__'
        #exclude = ['monto']
        fields = ['check_in',
        'check_out', 'adultos', 'ninios', 'telefono', 'comentario']
        

        comentario= forms.CharField(widget=forms.Textarea(attrs={'rows':3})) 
        widgets = {
            "check_in": DatePickerInput(options={"format": "MM/DD/YYYY"}),
            "check_out": DatePickerInput(options={"format": "MM/DD/YYYY"}),
           # 'check_in': forms.DateInput(format=('%d-%m-%Y'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),
            #'check_out': forms.DateInput(format=('%d-%m-%Y'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),
            
        }
        

        