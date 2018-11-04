from .exception import duplicateException

def checkDublicate(klass,_self,**kwargs):
    q = klass.objects.filter(**kwargs)
    if q.exists() and _self.pk != q[0].pk :# should not a name duplicate
            raise duplicateException('this {} is alredy exist'.format(kwargs))
