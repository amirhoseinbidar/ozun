from django.core.exceptions import ValidationError

class membershipException(ValidationError):
    def __init__(self ,*args , **kwargs):
        self.code = 'membershipException'
        super(membershipException,self).__init__(*args,**kwargs)

class duplicateException(ValidationError):
    def __init__(self,*args,**kwargs):
        self.code = 'duplicateException'
        super(duplicateException,self).__init__(*args,**kwargs)

class unequalityException(ValidationError):
    def __init__(self,*args,**kwargs):
        self.code = 'unequalityException'
        super(unequalityException,self).__init__(*args,**kwargs)
