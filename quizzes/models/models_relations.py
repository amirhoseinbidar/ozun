# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .models_quiz import Answer , User,Quiz ,membershipException 
from users.models import BaseTemporaryKey
from django.utils import timezone
from core.exceptions import ValidationError , duplicationException
from django.utils.crypto import get_random_string
from django.db.models import Sum

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
            flag = self.quiz.answers.filter(pk = self.user_answer.pk).exists()            
        
        if flag:
            return super(self.__class__, self).save(*args,**kwargs)
    
        raise membershipException(message =  'user_answer should be one of the quiz.answers')
    class Meta:
        verbose_name_plural = 'Quizzes_Statuses'


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


class Exam(BaseTemporaryKey):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length = 100 , blank = True)
    is_active = models.BooleanField() 
    
    def create_record(self,user,key=None,ignore_key_exception =True
        , forward_time = 0,is_active = True,*args,**kwargs ): 
        if not key:
            key = get_random_string()
        
        if not ignore_key_exception :
            if Exam.objects.filter(key = key).exists():# should not a key duplicate
                raise ValidationError('this key is alredy exist')
        
        else:
            while True:
                if Exam.objects.filter(key = key).exists():# should not a key duplicate
                    key = get_random_string()
                    continue
                break 
        
        if Exam.objects.filter(user = user , is_active = True).exists():
            raise duplicationException('a active exam alredy exist first close it')

        super(Exam,self).create_record(forward_time,*args,**kwargs)
        self.key = key
        self.is_active = is_active
        self.user = user
        self.save()
        return self

    def isOutOfDate(self):
        if timezone.now() >= self.close_date:
            return True   
        return False 

    def disable(self):
        self.is_active = False
        self.key = ''
        self.save()
    
    def cleaner_action(self):
        self.disable()
    
    def __unicode__(self):
        if timezone.now() > self.close_date :
            return u'key {0} is out of date'.format(self.key)
        return u'key: {0} ;;; {1} later will delete'.format(self.key,self.close_date - timezone.now() )
    
    @staticmethod
    def create_exam(quizzes,user):
        forward_time = quizzes.aggregate(Sum('time_for_out'))
        exam = Exam.create_record(user = user
            ,forward_time=forward_time.second)
        
        statuses_data = [ QuizStatus(quiz = quiz , 
            user_answer = None,exam = exam) for quiz in quizzes ]
        
        QuizStatus.objects.bulk_create(statuses_data)

        return exam
           
