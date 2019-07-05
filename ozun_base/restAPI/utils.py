from core.models import LessonTree ,TreeContent  ,allowed_types 
from rest_framework.exceptions import NotFound , NotAcceptable 
from quizzes.models import Source 
from django.core.exceptions import  ValidationError , ObjectDoesNotExist
from rest_framework.permissions import BasePermission , SAFE_METHODS
from rest_framework import viewsets , mixins
from rest_framework.pagination import LimitOffsetPagination

def checkLessonTreeContent(content , _type , field_name ,is_slug =True):
    try:
        obj = LessonTree.find_by_path(content , is_slug)
        allowed_types(_type , obj , field_name )
        return obj
    except ObjectDoesNotExist :
        raise NotFound('lesson path is not exist ' )
    except ValidationError as e:
        raise NotAcceptable(e.message)

def checkSourceContent(content):
    try:
        return Source.objects.get(name = content)
    except ObjectDoesNotExist:
        raise NotFound('this source is not exist')


class IsOwner(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True
        user = getattr(obj , 'user' , None) or getattr(obj , 'added_by' , None)
        if not user:
            return True

        return user == request.user
        
class IsOwnerMixin(object):
    def get_permissions(self):
        permissions = super().get_permissions()
        permissions.append(IsOwner())
        return permissions


class WriteOnlyViewSetMixin(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet ):
        pass


def LimitOffsetPaginationWrapper(default_limit = 10):
    lop = LimitOffsetPagination
    lop.default_limit = default_limit
    return lop
