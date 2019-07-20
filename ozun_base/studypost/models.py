# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from core.models import MediaConnect , SlugModel ,FeedBack , MediaConnect ,LessonTree  
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation 
from core.utils import get_all_related_lessonTree
from collections import Counter


class StudySubPost(models.Model):
    content = RichTextUploadingField()
    media = GenericRelation(MediaConnect)
    lesson = models.ForeignKey(LessonTree, null=True,
                               blank=True, on_delete=models.SET_NULL) 
    @property
    def get_lesson(self):
        if self.lesson:
            return self.lesson.full_path_slug
        return ''
    
    @classmethod
    def get_by_path(cls , lesson_path,get_by_slug =True):
        return get_all_related_lessonTree( cls, 'lesson' , lesson_path , get_by_slug )

    class Meta:
        abstract = True
 

class StudyPost(SlugModel):
    title = models.CharField(unique=True , max_length = 255 , blank=False) 
    content = RichTextUploadingField()
    image = models.ImageField()
    media = GenericRelation(MediaConnect) # it is for content media 

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    lesson = models.ForeignKey(LessonTree, null=True,
                               blank=True, on_delete=models.SET_NULL)
    
    total_votes = models.IntegerField(default=0)
    votes = GenericRelation(FeedBack)
    
    def count_votes(self):
        """Method to update the sum of the total votes. Uses this complex query
        to avoid race conditions at database level."""
        dic = Counter(self.votes.values_list("feedback_type", flat=True))
        self.__class__.objects.filter(id=self.id).update(
            total_votes=dic['U'] - dic['D'])
        self.refresh_from_db()

    @property
    def get_lesson(self):
        if self.lesson:
            return self.lesson.full_path_slug
        return ''
 
    @classmethod
    def get_by_path(cls , lesson_path,get_by_slug =True):
        return get_all_related_lessonTree( cls, 'lesson' , lesson_path , get_by_slug )

    class Meta:
        abstract = True


# NOTE: magazine and course are exaclly same but for diffrent purpose
#       magazine is often long text talk about two or more same thing
#       course is a short content talk about a subject


class Magazine(StudyPost):
    pass

class Course(StudyPost):
    pass

class CourseSubPost(StudySubPost):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='sub_posts' )
