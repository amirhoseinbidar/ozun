# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics 
from restAPI.serializers import  Quiz , ExamSerializer,ExamListSerializer , QuizStatusSerializer  
from quizzes.models import Exam,Source ,Quiz
from quizzes import utils
from core.exceptions import duplicationException
from rest_framework.exceptions import UnsupportedMediaType , NotFound , ParseError , NotAuthenticated ,APIException
from core.utils import find_in_dict
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

class StartExam(generics.ListAPIView):
    
    serializer_class = ExamListSerializer
    
    def get_queryset(self):
        data = self.request.query_params
        level = data.get('level' , None)
        source = data.get('source' , None)
      
        try:
            number = data.get('number' ,None)
            if number:
                number = int(number)
            return Exam.start_random_exam(self.kwargs["LessonPath"], 
                        user = self.request.user , level = level , 
                        source = source ,number = number  )

        except (duplicationException, ValidationError) as e:
            raise ParseError(e,400)
        except ValueError:
            raise ParseError('number parametr must be digit')

        

class CheckHaveOpenExamMixin():
    def check_exam(self):        
        q = self.get_queryset()
        if not q.exists():
            raise NotFound('you have not any open Exam')
        return q
    
class UpdateExam(generics.GenericAPIView  , CheckHaveOpenExamMixin, 
            generics.mixins.UpdateModelMixin):
    
    def get_queryset(self):
        return Exam.objects.filter(user = self.request.user , is_active = True)
    def get_object(self):
        return Exam.objects.get(user = self.request.user , is_active = True)
    
    def check_content_type(self,*args,**kwargs):
        if self.request.content_type != 'application/json':
            raise UnsupportedMediaType('only "application/json" content_type allowed ') 
    
    serializer_class = ExamSerializer

    def put(self,request,*args,**kwargs):
        self.check_content_type()
        self.check_exam()
        return self.update(request, paritial = True ,  *args,**kwargs)
    
    
class FinishExam(generics.views.APIView , CheckHaveOpenExamMixin):
    def get_queryset(self):
        return Exam.objects.filter(user = self.request.user , is_active = True)

    def get(self,request,*args,**kwargs):
        exam = self.check_exam()[0]
        exam.disable().save()
        data = {
            'notification' : 'exam finished successfully',
            'exam_pk' : exam.pk,
            'add_date' : exam.add_date,
            'close_date' : exam.close_date, 
        }
        return Response(data , status.HTTP_200_OK )

class ExamInfo(generics.ListAPIView):#TODO: ExamStatistics
    serializer_class = ExamListSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('exam_id')
        if pk == 'active':
            return Exam.objects.filter(user = self.request.user , is_active = True)
        
        if pk.isdigit():
            exam = Exam.objects.filter(pk =pk)
            if exam.exists():
                if exam[0].user.pk == self.request.user.pk:
                    return exam
                raise NotAuthenticated('you cant access to this exam , this is not for you ')
    
        raise ParseError('uncorrect arguments')
