# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import ContentType , GenericForeignKey
from django.contrib.auth.models import User
from core.models import LessonTree
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class StudyPost(models.Model):
    content = MarkdownxField()

    timestamp = models.DateTimeField(auto_now_add=True)
    add_by = models.ForeignKey(User,blank = True
        ,null = True , on_delete=models.SET_NULL)
    lesson = models.ForeignKey(LessonTree,null = True,
        blank = True , on_delete=models.SET_NULL) 

    def get_markdownfy(self):
        return markdownify(self.content)
    
    class Meta:
        abstract = True   

##NOTE magazine and course are exaclly same but for diffrent purpose

class magazine(StudyPost):
    pass

class course(StudyPost):
    pass 
