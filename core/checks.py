from .exceptions import duplicationException

def checkDublicate(klass,_self,objects = None,**kwargs):
    
    if objects:
        q = objects.filter(**kwargs).exclude(pk = _self.pk)
    else:
        q = klass.objects.filter(**kwargs).exclude(pk = _self.pk)
    if q.exists():# should not a name duplicate 
        raise duplicationException('this {} is alredy exist'.format(kwargs))
