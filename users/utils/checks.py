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


    


# our algorith clear out of date quizzes immediately 
# or at worst with 1 minute delay it is possible that it clear quiz and its data through 
# process and make problem it happen when the time of process start and 
# the time of out is very close 
#class ignoreQuizlose():
#    def __init__(self,f):
#        self.function = f
#    def __call__(self,*args,**kwargs):
#        try :
#            return self.function(*args,**kwargs)
#        except ObjectDoesNotExist:
#            return redirect('/profile/')

