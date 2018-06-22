from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class registerForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(max_length=254 ,
        widget= forms.PasswordInput , label = 'password')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
       
