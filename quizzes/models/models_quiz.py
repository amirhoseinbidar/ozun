# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import Counter

from django.db import models
from studylab.settings import BASE_DIR
from core.exceptions import membershipException,ValidationError
import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from core.checks import checkDuplicate
from django.dispatch import receiver
from django.db.models.signals import post_save
from quizzes.utils import getTimeByLevel
from users.models import FeedBack
from core.models.lessonTree import(allowed_types ,LESSON 
    , GRADE ,TOPIC ,CHAPTER ,LessonTree)
from course.models import StudyPostBase

class Source(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Answer(models.Model):
    post = GenericRelation( StudyPostBase )
    is_correct_answer = models.BooleanField()
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    def __unicode__(self):
        return u'answer id: {0}'.format(self.pk)
    def save(self,*args,**kwargs):
        if self.is_correct_answer:
            checkDuplicate(Answer,self, is_correct_answer=True )
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
    
    image = models.ImageField(blank = True,null = True,
         upload_to = 'quizzes/images')
    
    exponential_answer=GenericRelation(StudyPostBase,blank = True , null = True)
    
    source = models.ForeignKey(Source ,null = True,
        blank=True, on_delete=models.SET_NULL)
    level = models.CharField(max_length = 2,choices =LEVEL_TYPE )
    lesson = models.ForeignKey(LessonTree,null = True,
        blank = True , on_delete=models.SET_NULL) 

    time_for_out = models.TimeField(blank = True , null = True)
    added_by = models.ForeignKey(User,null = True , blank = True 
        , on_delete = models.SET_NULL)
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

    
    
    def save(self,*args,**kwargs): 
        allowed_types([LESSON ,CHAPTER ,TOPIC ],self.lesson ,'lesson' )
       
        if not self.time_for_out:
            self.time_for_out = getTimeByLevel(self.level)
        super(Quiz,self).save(*args,**kwargs)
        
        
    
    def __unicode__(self):
        return u'{0}'.format(self.pk)
    
    class Meta:
        ordering = ['-timestamp']

@receiver(post_save , sender= Quiz)
def voteUpdate(instance,created,**kwargs):
    instance.count_votes()