from django.http import Http404 
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def check_user_is_own(request  , to , attr = 'pk'):
    '''attr: by which attrebute you want authenticate 
        to : with what'''
    if not request.user.is_authenticated:# is user logined
        return False
    elif getattr(request.user,attr) != to :# is opened page for this user 
        return False
    else:
        return True 


    

