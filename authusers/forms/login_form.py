from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 120, \
        widget = forms.TextInput(attrs = {'required' : 'true', 'placeholder' : 'Username', 'class' :'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput\
        (attrs = {'required' : 'true', 'placeholder' : 'Password', 'class' :'form-control'}))
