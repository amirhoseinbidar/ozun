# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from core.models import LessonTree 
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from core.models import MediaConnect

class StudyPost(models.Model):
    content = RichTextUploadingField()
    
    media = GenericRelation(MediaConnect)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    add_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    lesson = models.ForeignKey(LessonTree, null=True,
                               blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

# NOTE: magazine and course are exaclly same but for diffrent purpose
#       magazine is often long text talk about two or more same thing
#       course is a short content talk about a subject

class magazine(StudyPost):
    pass


class course(StudyPost):
    pass
