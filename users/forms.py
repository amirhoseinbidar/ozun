from django import forms

class loginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput , min_length=8 )

class registerForm(forms.Form):
    username = forms.CharField(min_length=4,max_length=20)
    
    password = forms.CharField(
        min_length=8 ,widget= forms.PasswordInput )
    
    re_password = forms.CharField(
        min_length=8 ,widget= forms.PasswordInput 
        , label='please enter password again')
    
    email = forms.EmailField()

    