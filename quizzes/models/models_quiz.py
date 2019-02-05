# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import Counter
from django.db import models
from core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from core.checks import checkDuplicate
from quizzes.utils import getTimeByLevel
from users.models import FeedBack
from core.models.lessonTree import(allowed_types ,LESSON 
                    ,TOPIC ,CHAPTER ,LessonTree)
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from core.exceptions import duplicationException

class Source(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return u'{0}'.format(self.name)

    def save_or_get(self,*args,**kwargs):
        try:
            checkDuplicate(Source,self,name = self.name)
        except duplicationException :
            return Source.objects.get(name = self.name)
        self.save()
        return self


class Answer(models.Model):
    content = MarkdownxField()
    is_correct_answer = models.BooleanField()
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    
    def __unicode__(self):
        return u'answer id: {0}'.format(self.pk)
   
    def save(self,*args,**kwargs):
        if self.is_correct_answer:
            checkDuplicate(Answer,self, is_correct_answer=True , quiz = self.quiz)

        super(Answer,self).save(*args,**kwargs)    

    def get_markdownify(self):
        return markdownify(self.content)


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
    REVERS_LEVEL_TYPE = (
        ('very hard' , VERY_HARD),
        ('hard' , HARD),
        ('medium' , MEDIUM),
        ('easy',EASY),
        ('very easy', VERY_EASY),
    )

    content = MarkdownxField()
    votes = GenericRelation(FeedBack)
    total_votes = models.IntegerField(default=0)
    exponential_answer = MarkdownxField(blank=True)
    source = models.ForeignKey(Source ,null = True, blank=True, on_delete=models.SET_NULL)
    level = models.CharField(max_length = 2,choices =LEVEL_TYPE )
    lesson = models.ForeignKey(LessonTree,null = True, blank = True , on_delete=models.SET_NULL) 
    time_for_out = models.TimeField(blank = True , null = True)
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
        return Quiz.objects.order_by('-total_votes')[_from:to] 

    @staticmethod
    def get_by_path(lesson_path):
        branch = LessonTree.find_by_path(lesson_path)
        lessons = list(branch.get_descendants())+[branch]
        quizzes =Quiz.objects.filter( 
            lesson__in = lessons )
            
        return quizzes

    def save(self,*args,**kwargs): 
        allowed_types([LESSON ,CHAPTER ,TOPIC ],self.lesson ,'lesson' )
       
        if not self.time_for_out:
            self.time_for_out = getTimeByLevel(self.level)
        super(Quiz,self).save(*args,**kwargs)
        
        self.count_votes()    
    
    def __unicode__(self):
        return u'{0}'.format(self.pk)
    
    def get_markdownify_content(self):
        return markdownify(self.content)
    
    def get_markdownify_EA(self):
        return markdownify(self.exponential_answer)

    class Meta:
        ordering = ['-timestamp']
