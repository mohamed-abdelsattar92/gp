from django import forms
from django.core.validators import RegexValidator


class NameForm(forms.Form):
    first_name = forms.CharField(
        widget = forms.TextInput(attrs = {'required':'true', 'class':'form-control', 'placeholder':'Technician First Name'})
    )
    middle_name = forms.CharField(
        widget = forms.TextInput(attrs = {'required':'true', 'class':'form-control', 'placeholder':'Technician Middle Name'})
    )
    last_name = forms.CharField(
        widget = forms.TextInput(attrs = {'required':'true', 'class':'form-control', 'placeholder':'Technician Last Name'})
    )


class SkillForm(forms.Form):
    skill = forms.CharField(
        widget = forms.TextInput(attrs = {'required':'true', 'class':'form-control', 'placeholder':'Technician Skill'})
    )


class LocationForm(forms.Form):
    longitude = forms.FloatField(
        widget = forms.HiddenInput()
    )
    latitude = forms.FloatField(
        widget = forms.HiddenInput()
    )
