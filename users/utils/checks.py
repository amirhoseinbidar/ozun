from django.http import Http404
from django.contrib.auth.models import User


def check_user_exists(*args,**kwargs):
    '''check user by what coder want usaully by username or pk'''
    if  User.objects.filter(*args,**kwargs).exists():
        return True
    else :
        return False

class check_user_exists_decorator(object):
    '''
        every function witch use this this decorator should have a "attr" argomant
        with specified filterd by which one attrebute
    '''
    def __init__(self,function):
        self.function = function
       
    def __call__(self,*args,**kwargs):

        attr =kwargs.get('attr')
        attr_value=kwargs.get(attr)
        
        flag = check_user_exists(**{'{0}'.format(attr) : '{0}'.format(attr_value)})

        if flag:
            return self.function(*args,**kwargs)
        else:
            raise Http404()


def check_user_is_own(request , attr , to):
    '''attr: by which attrebute you want authenticate 
        to : with what'''
    if not request.user.is_authenticated():# is user logined
        print False,1
        return False
    elif getattr(request.user,attr) != long(to) :# is opened page for this user 
        print False,2
        return False
    else:
        print True
        return True 
