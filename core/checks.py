from .exceptions import duplicationException

def checkDuplicate(klass,_self,objects = None,**kwargs):
    
    if objects:
        q = objects.filter(**kwargs).exclude(pk = _self.pk)
    else:
        q = klass.objects.filter(**kwargs).exclude(pk = _self.pk)
    if q.exists():# should not a name Duplicate 
        raise duplicationException('this {} is alredy exist'.format(kwargs))
