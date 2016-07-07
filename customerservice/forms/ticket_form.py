from django import forms
from django.core.validators import RegexValidator
from ticket.models import Ticket

class TicketForm(forms.Form):
    STATUS_CHOICES = (
        ('OP','Open'),
        ('AS', 'Assigned'),
        ('WP', 'Work In Progress'),
        ('FL','Need Follow Up'),
        ('CL', 'Closed'),
    )
    problem_title = forms.CharField(max_length = 100,\
        widget = forms.TextInput(attrs = {'required':'true','placeholder':'Problem Title', 'class':'form-control'}))
    problem_description = forms.CharField(widget = forms.Textarea(attrs = {'placeholder':'Prolem Description', \
    'required':'true', 'class':'form-control'}))
    status = forms.ChoiceField(choices = STATUS_CHOICES,widget = forms.Select(attrs = {'class':'form-control'}))
