from django.db import models
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey ,GenericRelation

def file_folder(instance , filename):
    if isinstance(instance ,MediaConnect):
        return 'media/{}'.format(filename)
    if isinstance(instance ,BaseFileConnect):
        return 'file/{}'.format(filename)
    
    return filename


class GeneralFileConnectBase(models.Model):
    ''' 
        general file model is a abstract model use in models that use as reverse
        forgien key in another models 
    '''
    file = models.FileField(upload_to=file_folder, default='')
    mime = models.CharField(max_length=64, blank=True)
   

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

class MediaConnect(GeneralFileConnectBase):
    ''' images and videos that should show to another users should save here '''
    image_1 = models.ImageField(upload_to = file_folder , blank = True , null = True)
    image_2 = models.ImageField(upload_to = file_folder , blank = True , null = True)
    is_optimized = models.BooleanField(default=False) 
    is_broken = models.BooleanField(default=False)

class DiscoverMediaMixin(object):
    ''' 
        media that add from admin add from editor and editor dont add them atumaticlly to media connect
        so this mixin check content(s) and add founded media to MediaConnect 
    '''

class BaseFileConnect(GeneralFileConnectBase):
    ''' 
    files that do not have specific format or purpose should store here it is abstract model
    another models can override it 
    '''
    class Meta:
        abstract = True

## we strill dont neet this class
#class FileConnect(BaseFileConnect):
#    ''' 
#    files that do not have specific format or purpose should store here 
#    '''
#    pass