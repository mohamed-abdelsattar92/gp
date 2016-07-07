from django import forms
from django.forms import TextInput
from django.core.validators import RegexValidator
from ..models import Customer


class CustomerForm(forms.Form):
    first_name = forms.CharField(
        max_length = 120,
        widget = TextInput(attrs = {'required':'true', 'placeholder':'First Name', 'class':'form-control'}))
    middle_name = forms.CharField(
        max_length = 120,
        widget = TextInput(attrs = {'required':'true', 'placeholder':'Middle Name', 'class':'form-control'}))
    last_name = forms.CharField(
        max_length = 120,
        widget = TextInput(attrs = {'required':'true', 'placeholder':'Last Name', 'class':'form-control'}))
    mobile_number = forms.CharField(
        max_length = 11,\
        widget = TextInput(attrs = {'required':'true', 'placeholder':'Mobile Phone', 'class':'form-control'}),\
        validators = [RegexValidator(r'01\d{9}',"Please enter a valid mobile number.")])
    land_phone_number = forms.CharField(
        max_length = 8,\
        widget = TextInput(attrs = {'required':'true', 'placeholder':'Landline Phone', 'class':'form-control'}),\
        validators = [RegexValidator(r'\d{8}',"Please enter a valid land_phone_number")])
    address_formated = forms.CharField(
        max_length = 200,\
        widget = TextInput(attrs = {'required':'true', 'placeholder':'Address', 'class':'form-control'}))
    longitude = forms.FloatField()
    latitude = forms.FloatField()
