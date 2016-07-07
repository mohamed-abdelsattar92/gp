from django import forms
from django.core.validators import RegexValidator


class ViewTicketForm(forms.Form):
    opened = forms.BooleanField(required = False)
    assigned = forms.BooleanField(required = False)
    work_in_progress = forms.BooleanField(required = False)
    follow_up = forms.BooleanField(required = False)
