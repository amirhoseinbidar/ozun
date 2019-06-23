from .exceptions import duplicationException, ValidationError
from rest_framework.exceptions import ParseError

def checkDuplicate(klass, _self, objects=None, **kwargs):
    if objects:
        q = objects.filter(**kwargs).exclude(pk=_self.pk)

    else:
        q = klass.objects.filter(**kwargs).exclude(pk=_self.pk)
    if q.exists():  # should not a name Duplicate
        raise duplicationException('this {} is alredy exist'.format(kwargs))


class APIExceptionHandler(object):
    def handel_exception(self,method,args,kwargs):
        try:
            return getattr(super(),method)(*args,**kwargs)
        except ValidationError as e:
            raise ParseError(e.message)

    def post(self,*args,**kwargs):
        return self.handel_exception('post',args,kwargs)
    def put(self,*args,**kwargs):
        return self.handel_exception('put',args,kwargs)
    def patch(self,*args,**kwargs):
        return self.handel_exception('patch',args,kwargs)
    def delete(self,*args,**kwargs):
        return self.handel_exception('delete',args,kwargs)
    def get(self,*args,**kwargs):
        return self.handel_exception('get',args,kwargs)
    