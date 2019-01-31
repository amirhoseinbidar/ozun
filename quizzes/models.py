# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class source(models.Model):
    sources = models.CharField(max_length=50)
    class Meta:
        db_table = "sources"
    def __unicode__(self):
        return u'{0}'.format(self.sources)


class level(models.Model):
    levels = models.CharField(max_length= 20)
    class Meta:
        db_table = "levels"
    def __unicode__(self):
        return u'{0}'.format(self.levels)

class lesson(models.Model):
    lessons = models.CharField(max_length= 30)
    class Meta:
        db_table = "lessons"
    def __unicode__(self):
        return u'{0}'.format(self.lessons)


class grade(models.Model):
    grades = models.CharField(max_length= 30)
    class Meta:
        db_table = "grades"
    def __unicode__(self):
        return u'{0}'.format(self.grades)

class quizze(models.Model):
    text = models.TextField()
    answer = models.TextField()
    correct_answer = models.CharField(max_length= 100)
    
    exponential_answer= models.FilePathField(
        allow_folders=True,
        path='/home/abk/bigEpsilon/studylab/exponential answers' ,
        )

    source = models.ForeignKey(source)
    level = models.ForeignKey(level)
    lesson = models.ForeignKey(lesson)
    grade = models.ForeignKey(grade)
    class Meta:
        db_table = "quizzes"
    def __unicode__(self):
        return u'{0}'.format(self.pk)



    