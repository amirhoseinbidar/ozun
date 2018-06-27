import threading
from users.models import Email_auth 
from django.utils import timezone

# every 30 minute check email_auth  table
# and delete who remove_date of record is passed 
def run_cleaner():   
    now = timezone.now()
    records = Email_auth.objects.all()
    for record in records:
        if record.remove_date < now:
            record.delete()
    threading.Timer(600.0, run_cleaner).start()

########################
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

########################
from django import forms
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from users.models import Profile

class registerForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(max_length=254 ,
        widget= forms.PasswordInput , label = 'password')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class profileForm(forms.ModelForm):
    firs_name = forms.CharField(max_length=254)
    last_name = forms.CharField(max_length=254)
    

    class Meta:
        model = Profile
        fields = ('image' , 'bio' , 'location' , 'brith_day' )


#########################
from django.http import Http404



def check_user_exists(username):
    
    if  User.objects.filter( username=username).exists():
        return True
    else :
        return False

class check_user_exists_decorator(object):
    def __init__(self,function):
        self.function = function

    def __call__(self,*args,**kwargs):
        flag = check_user_exists(kwargs.get('username'))
        
        if flag:
            return self.function(*args,**kwargs)
        else:
            raise Http404()


def check_user_is_own(request , username):
    if not request.user.is_authenticated():
        return False
    elif request.user.username != username :
        return False
    else:
        return True 
