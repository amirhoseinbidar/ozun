# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import Counter

from django.db import models
from studylab.settings import BASE_DIR
from core.exception import membershipException,ValidationError
import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from core.checks import checkDublicate
from django.dispatch import receiver
from django.db.models.signals import post_save
from quizzes.quizzes_utils import getTimeByLevel
from users.models import FeedBack
from core.models.lessonTree import(allowed_types ,LESSON 
    , GRADE ,TOPIC ,LessonTree)

class Source(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Exponential_answer(models.Model):
    text = models.TextField(blank = True)
    image = models.ImageField(blank = True,null = True,upload_to='exponential_answers/images')
    video = models.FileField(blank = True,null = True,upload_to='exponential_answers/videos')
    extra = models.FileField(blank = True,null = True,upload_to='exponential_answers/extras')
    #mybe something else will add 
    def __unicode__(self):
        return u'{0}'.format(self.pk)

class Answer(models.Model):
    text = models.TextField()
    is_correct_answer = models.BooleanField()
    quiz = models.ForeignKey('Quiz')
    def __unicode__(self):
        return u'answer id: {0}'.format(self.pk)
    def save(self,*args,**kwargs):
        if self.is_correct_answer:
            checkDublicate(Answer,self, is_correct_answer=True )
        super(Answer,self).save(*args,**kwargs)




class Quiz(models.Model):
    VERY_HARD = 'VH'
    HARD = 'H'
    MEDIUM = 'M'
    EASY = 'E'
    VERY_EASY = 'VE'
    LEVEL_TYPE = (
        (VERY_HARD , 'very hard'),
        (HARD , 'hard'),
        (MEDIUM , 'medium'),
        (EASY , 'easy'),
        (VERY_EASY , 'very easy'),
    )
    
    text = models.TextField()
    votes = GenericRelation(FeedBack)
    total_votes = models.IntegerField(default=0)
    models.ImageField()
    image = models.ImageField(blank = True,null = True, upload_to = 'quizzes/images')
    exponential_answer= models.ForeignKey(to = Exponential_answer,blank= True,null = True )
    source = models.ForeignKey(Source)
    level = models.CharField(max_length = 2,choices =LEVEL_TYPE )
    lesson = models.ForeignKey(LessonTree) 

    time_for_out = models.TimeField()
    added_by = models.ForeignKey(User,null = True , blank = True , on_delete = models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def count_votes(self):
        dic = Counter(self.votes.values_list("feedback_type", flat=True)) 
        Quiz.objects.filter(id=self.id).update(
            total_votes=dic[FeedBack.UP_VOTE] - dic[FeedBack.DOWN_VOTE])
        self.refresh_from_db()
    
    @staticmethod
    def get_mostVotes(_from,to):
        """ return a list of most Voted quizzes by area"""
        if not ( to > _from and to >=1 and _from >= 1 ):
            raise  ValidationError(''''one of argomants are negative or
                zero or "to <= _from" ''')
        return Quiz.objects.orderby('-total_votes')[_from:to] 

    

    def isTopicsFieldValid(self):
        return self.topics.filter(lesson__pk = self.lesson.pk).count() == self.topics.count()
        # is all of the topics from determined lesson  
    
    @allowed_types([ LESSON , GRADE ,TOPIC ],lesson)
    def save(self,*args,**kwargs):
        if not self.time_for_out:
            self.time_for_out = getTimeByLevel(self.level)
        
        super(Quiz,self).save(*args,**kwargs)
        
        
    
    def __unicode__(self):
        return u'{0}'.format(self.pk)
    
    class Meta:
        ordering = ['-timestamp']

receiver(post_save , sender= Quiz)
def voteUpdate(instance,created,**kwargs):
    if created:
        instance.count_votes()