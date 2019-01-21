from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models.countries import Country_province, Country_county, Country_city

from generics.forms import ListTextWidget ,find_datas
from users.models import Profile


class signUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(
        max_length=254, widget=forms.PasswordInput, label='password')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email = email).exists():
            raise forms.ValidationError('A user with that email already exists.')
       
        return email


 

