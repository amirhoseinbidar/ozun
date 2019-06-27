# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from core.models import LessonTree 
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from core.models import MediaConnect , SlugModel 
from core.models import FeedBack , MediaConnect
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation

class StudyPost(SlugModel):
    title = models.CharField(unique=True , max_length = 255 , blank=False) 
    content = RichTextUploadingField()
    media = GenericRelation(MediaConnect)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    lesson = models.ForeignKey(LessonTree, null=True,
                               blank=True, on_delete=models.SET_NULL)
    

    votes = GenericRelation(FeedBack)
    tags = TaggableManager()
    media = GenericRelation(MediaConnect)
    
    @property
    def get_lesson(self):
        if self.lesson:
            return self.lesson.full_path
        return ''

    class Meta:
        abstract = True

# NOTE: magazine and course are exaclly same but for diffrent purpose
#       magazine is often long text talk about two or more same thing
#       course is a short content talk about a subject

class Magazine(StudyPost):
    
    @staticmethod
    def get_by_path(lesson_path,get_by_slug =True):
        return get_all_related_lessonTree( Magazine, 'lesson' , lesson_path , get_by_slug )



class Course(StudyPost):

    @staticmethod
    def get_by_path(lesson_path,get_by_slug =True):
        return get_all_related_lessonTree(Course, 'lesson' , lesson_path , get_by_slug )

