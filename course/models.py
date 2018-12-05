# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import ContentType , GenericForeignKey
from django.contrib.auth.models import User
from core.models import LessonTree

#in fact it is better to valid all files then save is it in computer at one 
#class use of 'pip install filetype' for doing this process

class StudyMedia(models.Model):
    image = models.ImageField(blank = True,
        null = True ,upload_to= 'StudyPost/images')
    post = models.ForeignKey('StudyPostBase', on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Mediums"

#class StudyVideo(models.Model): #use of file field is not secure
#    video = models.FileField(blank = True, null = True 
#        ,upload_to= 'StudyPost/images')
#    post = models.ForeignKey('StudyPostBase', on_delete=models.CASCADE)
#    class Meta:
#        verbose_name = "Video"
#        verbose_name_plural = "Videos"

class StudyPostBase(models.Model): #NOTE: it will use is quizzes part
    text = models.TextField()
    
    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

class StudyPost(models.Model):
    post = models.ForeignKey(StudyPostBase, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    add_by = models.ForeignKey(User,blank = True
        ,null = True , on_delete=models.SET_NULL)
    lesson = models.ForeignKey(LessonTree,null = True,
        blank = True , on_delete=models.SET_NULL) 