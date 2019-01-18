# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .models_quiz import Answer , User,Quiz ,membershipException 
from users.models import BaseTemporaryKey
from django.utils import timezone
from django.utils.timezone import timedelta
from core.exceptions import ValidationError , duplicationException
from django.utils.crypto import get_random_string
from django.db.models import Sum
from ..utils import turn_second_to_time

import datetime



class QuizStatus(models.Model):#RULE: user_answer  must be one of the quiz answers or None
    
    quiz = models.ForeignKey(Quiz , models.CASCADE)
    #NOTE : if use_answer be null mean user have not been replying  quiz
    user_answer = models.ForeignKey(Answer,blank = True,null = True , on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam' ,on_delete=models.CASCADE) 
    
    def save(self,*args,**kwargs):
        flag = False
        if not self.user_answer:# if user_answer is Null pass it
            flag = True
        
        else:
            flag = self.quiz.answer_set.filter(pk = self.user_answer.pk).exists()            
        
        if flag:
            return super(self.__class__, self).save(*args,**kwargs)
    
        raise membershipException(message =  'user_answer should be one of the quiz.answers')
    
    @staticmethod
    def saveFromQuizSet(quizzes):
        data = []
        for quiz in quizzes:
            quiz_status = Quiz_status(quiz = quiz,user_answer = None)
            quiz_status.save()
            data.append(quiz_status.pk)
        return Quiz_status.objects.filter(pk__in = data)
    
    @staticmethod
    def saveFromDict(dictionary):#RULL dictionary is like this {quiz_status_pk:##,answer_pk:##} 
        quiz =  Quiz_status.objects.get(pk = dictionary['quiz_status_pk'])
        quiz.user_answer = Answer.objects.get(pk = dictionary['answer_pk'])
        quiz.save()
        return quiz
    @staticmethod
    def saveFromDictList(data):
        List = []
        for dic in data:
            List.append(Quiz_status.saveFromDict(dic).pk)
        return Quiz_status.objects.filter(pk__in = List)

    class Meta:
        verbose_name_plural = 'Quizzes_Statuses'




class Exam(BaseTemporaryKey):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length = 100 , blank = True)
    is_active = models.BooleanField() 
    total_time = models.TimeField()
    
    def create_record(self,user,total_time,key=None,ignore_key_exception =True
            , forward_time = 0,is_active = True,*args,**kwargs ): 
        if not key:
            key = get_random_string()
        
        if not ignore_key_exception :
            if Exam.objects.filter(key = key).exists():# should not a key Duplicate
                raise ValidationError('this key is alredy exist')
        
        else:
            while True:
                if Exam.objects.filter(key = key).exists():# should not a key Duplicate
                    key = get_random_string()
                    continue
                break 
        
        if Exam.objects.filter(user = user , is_active = True).exists():
            raise duplicationException('a active exam alredy exist first close it')

        super(Exam,self).create_record(forward_time,*args,**kwargs)
        self.key = key
        self.is_active = is_active
        self.user = user
        self.total_time = total_time
        self.save()
        return self

    def isOutOfDate(self):
        if timezone.now() >= self.close_date:
            return True   
        return False 

    def disable(self):
        self.is_active = False
        self.key = ''
        self.close_date = timezone.now()
        #ExamStatistic(exam = self).save() ::TODO:: this is not prepare now
        return self
    
    def close_action(self):
        self.disable().save()
    
    def check_out_of_date(self):
        if self.is_active:
            return super().check_out_of_date()
        
    def __unicode__(self):
        if timezone.now() > self.close_date :
            return u'key {0} is out of date'.format(self.key)
        return u'key: {0} ;;; {1} later will delete'.format(self.key,self.close_date - timezone.now() )
    
    @staticmethod
    def get_total_time(quizzes):
        forward_time = timedelta(0) 
        for quiz in quizzes:   
            time = quiz.time_for_out
            forward_time += timedelta(hours = time.hour
                ,minutes = time.minute , seconds = time.second)
        return forward_time
    
    @staticmethod
    def create_exam(quizzes,user):
        #forward_time = quizzes.aggregate(Sum('time_for_out')) #Don't work in sqlite3
        forward_time = Exam.get_total_time(quizzes) 
        total_time = turn_second_to_time(forward_time.total_seconds())

        exam = Exam().create_record(user = user , total_time = total_time  
            , forward_time=forward_time.total_seconds())
        

        statuses_data = [ QuizStatus(quiz = quiz , 
            user_answer = None,exam = exam) for quiz in quizzes ]
        
        QuizStatus.objects.bulk_create(statuses_data)

        return exam



class ExamStatistic(models.Model):
    exam = models.OneToOneField(Exam,on_delete = models.CASCADE)
    negative_score = models.PositiveIntegerField()
    positive_score = models.PositiveIntegerField()
    total_score = models.IntegerField()
    advise = models.IntegerField()

    def create_exam_statistics(self,exam):
        pass 
