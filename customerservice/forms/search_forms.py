from django import forms
from django.core.validators import RegexValidator


class SearchByNameForm(forms.Form):
    name = forms.CharField(max_length = 120, \
        widget = forms.TextInput(attrs = {'required' : 'true', 'placeholder' : 'Customer Name', 'class' :'form-control'}))


class SearchByPhoneForm(forms.Form):
    phone = forms.CharField(max_length = 120, \
        widget = forms.TextInput(attrs = {'required' : 'true', 'placeholder' : 'Customer Phone Number',\
                                          'pattern':'\d{8}', 'title':'8-digits phone number', 'class' :'form-control'}),\
                                validators = [RegexValidator(r'\d{8}',"Please enter a valid phone number.")])
