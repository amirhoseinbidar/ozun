# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from studylab.settings import BASE_DIR
import os
# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        db_table = "sources"
    def __unicode__(self):
        return u'{0}'.format(self.name)


class Level(models.Model):
    name = models.CharField(max_length= 20)
    class Meta:
        db_table = "levels"
    def __unicode__(self):
        return u'{0}'.format(self.name)



class Grade(models.Model):
    name = models.CharField(max_length= 30)
    class Meta:
        db_table = "grades"
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Lesson(models.Model):
    grade = models.ForeignKey(Grade)
    name = models.CharField(max_length= 30)
    
    class Meta:
        db_table = "lessons"
    def __unicode__(self):
        return u'{0}/{1}'.format(self.grade.name,self.name)
class Chapter(models.Model):
    grade = models.ForeignKey(Grade)
    lesson = models.ForeignKey(Lesson)
    name = models.CharField(max_length = 100)
    class Meta:
        db_table = "chapter"
    def __unicode__(self):
        return u'{0}/{1}/{2}'.format(self.grade.name,self.lesson.name,self.name )
   
class Topic(models.Model):
    grade = models.ForeignKey(Grade)
    lesson = models.ForeignKey(Lesson)
    chapter = models.ForeignKey(Chapter)
    name = models.CharField(max_length = 100 , blank = True)
    class Meta:
        db_table = "topics"
    def __unicode__(self):
        return u'{0}/{1}/{2}/{3}'.format(self.grade.name,self.lesson.name,self.session.name,self.name )
class Exponential_answer(models.Model):
    text = models.TextField(blank = True)
    image = models.ImageField(blank = True,null = True,upload_to='exponential_answers/images')
    video = models.FileField(blank = True,null = True,upload_to='exponential_answers/videos')
    extra = models.FileField(blank = True,null = True,upload_to='exponential_answers/extras')
    #mybe something else add 
    def __unicode__(self):
        return u'{0}'.format(self.pk)

class Quizze(models.Model):
    text = models.TextField()
    answer = models.TextField()
    correct_answer = models.IntegerField()
     
    exponential_answer= models.OneToOneField(to = Exponential_answer,blank= True,null = True )
    source = models.ForeignKey(Source)
    level = models.ForeignKey(Level)
    
    topic = models.ManyToManyField(Topic)

    class Meta:
        db_table = "quizzes"
    def __unicode__(self):
        return u'{0}'.format(self.pk)