from django import forms
from django.core.validators import RegexValidator


class AssignTicketForm(forms.Form):
    date_of_visit = forms.DateField(
        widget = forms.DateInput(attrs = {'required':'true', 'type':'date', 'class':'form-control'})
    )
    time_of_visit = forms.TimeField(
        widget = forms.TextInput(attrs = {'required':'true', 'type':'time', 'class':'form-control'})
    )
