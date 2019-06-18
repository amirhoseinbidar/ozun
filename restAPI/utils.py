from core.models import LessonTree ,TreeContent  ,allowed_types 
from rest_framework.exceptions import NotFound , NotAcceptable 
from quizzes.models import Source 
from django.core.exceptions import  ValidationError , ObjectDoesNotExist
from core.models import Location

def checkLessonTreeContent(content , _type , field_name ,is_slug =True):
    try:
        obj = LessonTree.find_by_path(content , is_slug)
        allowed_types(_type , obj , field_name )
        return obj
    except ObjectDoesNotExist :
        raise NotFound('this {} is not exist'.format( dict(TreeContent.CONTENT_TYPE)[_type]  ) )
    except ValidationError as e:
        raise NotAcceptable(e.message)


def checkLocationContent(content):
    try:
        return Location.objects.get(path = content)
    except ObjectDoesNotExist:
        raise NotFound('this location is not exist')

def checkSourceContent(content):
    try:
        return Source.objects.get(name = content)
    except ObjectDoesNotExist:
        raise NotFound('this source is not exist')
