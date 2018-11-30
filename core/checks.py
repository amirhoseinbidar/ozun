from .exception import duplicateException

def checkDublicate(klass,_self,objects = None,**kwargs):
    
    if objects:
        q = objects.filter(**kwargs).exclude(pk = _self.pk)
    else:
        q = klass.objects.filter(**kwargs).exclude(pk = _self.pk)
    if q.exists():# should not a name duplicate 
        raise duplicateException('this {} is alredy exist'.format(kwargs))
