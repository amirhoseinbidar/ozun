# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .models_quiz import Answer , User,Quiz ,Source
from core.models import BaseTemporaryKey
from django.utils import timezone
from django.utils.timezone import timedelta
from core.exceptions import ValidationError , duplicationException ,membershipException
from django.utils.crypto import get_random_string
from django.db.models import Sum
from ..utils import turn_second_to_time , choice_without_repead ,calculate_score
from django.core.exceptions import ObjectDoesNotExist
from core.utils import find_in_dict 

from ozun.settings import DIFAULT_SEND_QUIZ
import datetime



class QuizStatus(models.Model):
    quiz = models.ForeignKey(Quiz , models.PROTECT)

    #RULE : user_answer  must be one of the quiz answers or None
    #       if user_answer be null mean user have not been replying  quiz
    user_answer = models.ForeignKey(Answer,blank = True,null = True , on_delete=models.SET_NULL)
    
    exam = models.ForeignKey('Exam' ,on_delete=models.CASCADE) 
    did_user_answer = models.BooleanField(default= False)
    
    def save(self,*args,**kwargs):
        flag = False
        if not self.user_answer:# if user_answer is Null pass it
            flag = True
        
        else:
            flag = self.quiz.answer_set.filter(pk = self.user_answer.pk).exists()            
        
        if flag:
            self.did_user_answer = True
            return super().save(*args,**kwargs)
    
        raise membershipException(message =  'user_answer should be one of the quiz.answers')
    
    class Meta:
        verbose_name_plural = 'Quizzes_Statuses'




class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField() 
    total_time = models.TimeField()        
    add_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    FORWARD_TIME = 600 # by second # 00:10:00

    def create_record(self,user,total_time, forward_time = 0,is_active = True,*args,**kwargs ): 

        if forward_time == 0:
            forward_time =self.FORWARD_TIME
        time = timezone.now()
        self.close_date = time + timezone.timedelta(0,forward_time)
        self.is_active = is_active
        self.user = user
        self.total_time = total_time
        self.save(*args,**kwargs)
        return self

    @staticmethod
    def has_user_active_exam(user):
        exams = Exam.objects.filter(user = user , is_active = True)
        if len(exams) != 0:
            flag = True
            for exam in exams:
                if exam.is_out_of_date():
                    exam.close_action()
                    flag = False
            return flag
        return False
        
    def is_out_of_date(self):
        if timezone.now() >= self.close_date:
            return True   
        return False 

    def disable(self):
        self.is_active = False
        ExamStatistic.create(exam = self) 
        return self
    
    def close_action(self):
        self.disable().save()
    
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

        exam = Exam().create_record(
            user = user , total_time = total_time  , 
            forward_time=forward_time.total_seconds()
        )
         
        statuses_data = [ 
            QuizStatus(quiz = quiz , user_answer = None,exam = exam) 
            for quiz in quizzes 
        ]
        
        QuizStatus.objects.bulk_create(statuses_data)

        return exam

    @staticmethod
    def start_random_exam( lesson_path , user ,is_path_slug =True, level=None , source =None, number=None):
        data = Exam.__order_optional_args(level,source,number)
        number = data.pop('number')

        quizzes = Quiz.get_by_path(lesson_path,is_path_slug).filter(**data )
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
            number = DIFAULT_SEND_QUIZ
        data['number'] = number

        return data


class ExamStatistic(models.Model):
    exam = models.ForeignKey(Exam,on_delete = models.CASCADE)
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
