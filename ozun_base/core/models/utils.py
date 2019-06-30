from django.db import models
from django.utils.text import slugify

class SlugModel(models.Model):
    ''' slug model for models that need slug its better use this model
        NOTE: "slug_field" determine field that should use for slugify '''
    slug = models.CharField(max_length=255, blank=True)
    slug_field = 'title' 
    def get_slug(self):
        return slugify(getattr(self,self.slug_field),True)
    
    def save(self,*args,**kwargs):
        self.slug = self.get_slug()
        return super().save(*args,**kwargs)

    class Meta:
        abstract = True