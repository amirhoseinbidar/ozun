# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .models_quiz import Answer , User,Quiz ,Source
from users.models import BaseTemporaryKey
from django.utils import timezone
from django.utils.timezone import timedelta
from core.exceptions import ValidationError , duplicationException ,membershipException
from django.utils.crypto import get_random_string
from django.db.models import Sum
from ..utils import turn_second_to_time , choice_without_repead ,calculate_score
from django.core.exceptions import ObjectDoesNotExist
from core.utils import find_in_dict 

import datetime



class QuizStatus(models.Model):#RULE: user_answer  must be one of the quiz answers or None
    
    quiz = models.ForeignKey(Quiz , models.CASCADE)
    #NOTE : if user_answer be null mean user have not been replying  quiz
    user_answer = models.ForeignKey(Answer,blank = True,null = True , on_delete=models.CASCADE)
    exam = models.ForeignKey('Exam' ,on_delete=models.CASCADE) 
    did_user_answer = models.BooleanField(default= False)
    
    def save(self,*args,**kwargs):
        flag = False
        if not self.user_answer:# if user_answer is Null pass it
            flag = True
        
        else:
            flag = self.quiz.answer_set.filter(pk = self.user_answer.pk).exists()            
        
        if flag:
            super().save(*args,**kwargs) # for ensure there is no problem
            self.did_user_answer = True
            return super().save(*args,**kwargs)
    
        raise membershipException(message =  'user_answer should be one of the quiz.answers')
    
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
        ExamStatistic.create(exam = self) 
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

    @staticmethod
    def start_random_exam( lesson_path , user , level=None , source =None, number=None):
        data = Exam.__order_optional_args(level,source,number)
        number = data.pop('number')

        quizzes = Quiz.get_by_path(lesson_path).filter(**data )
        quizzes = choice_without_repead(quizzes,number,False)

        
        exam = Exam.create_exam(quizzes,user)
        
        return Exam.objects.filter(pk = exam.pk)
    
    @staticmethod
    def __order_optional_args(level,source , number): 
        data = {}   
        if level : 
            if not find_in_dict(level, Quiz.LEVEL_TYPE) or not find_in_dict(level,Quiz.REVERS_LEVEL_TYPE):
                raise ValidationError('uncorrect level')
            
            data['level'] = dict(Quiz.REVERS_LEVEL_TYPE)[level]


        if source :
            try:
                data['source'] = Source.objects.get(name =source)
            except ObjectDoesNotExist:
                raise ValidationError('source does not exits')
        
        if not number:   
            number = 15
        data['number'] = number

        return data


class ExamStatistic(models.Model):
    exam = models.OneToOneField(Exam,on_delete = models.CASCADE)
    negative_score = models.PositiveIntegerField()
    positive_score = models.PositiveIntegerField()
    total_score = models.IntegerField()
    #advise = models.IntegerField()

    @staticmethod
    def create(exam):
        pos_score , neg_score = calculate_score(exam.quizstatus_set.all())
        total_score = pos_score - neg_score
        es = ExamStatistic(exam = exam , negative_score = neg_score ,
                positive_score = pos_score , total_score = total_score )
        es.save()
        return es
