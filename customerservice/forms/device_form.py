from django import forms
from django.core.validators import RegexValidator
from ..models import Device

class DeviceForm(forms.Form):
    model_name = forms.CharField(max_length = 100,\
                                widget = forms.TextInput(attrs={'required':'true', 'placeholder':'Model Name'}))
    serial_number = forms.CharField(max_length = 50,\
                                widget = forms.NumberInput(attrs={'required':'true', 'placeholder':'Serial Number'}))
    purchase_date = forms.CharField(max_length = 50,\
                                widget = forms.DateInput(attrs = {'type':'date', 'required':'true'}))
