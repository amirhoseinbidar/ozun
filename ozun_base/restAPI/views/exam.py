# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics 
from restAPI.serializers import  (
    ExamSerializer,
    ExamListSerializer , 
    ExamStartSerializer  
)  
from quizzes.models import Exam , Source ,Quiz
from quizzes import utils
from core.exceptions import duplicationException
from rest_framework.exceptions import (
    UnsupportedMediaType , NotFound ,
    ParseError , NotAuthenticated 
)
from core.utils import find_in_dict
from rest_framework import status , mixins 
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


class StartExam(mixins.ListModelMixin , generics.GenericAPIView):
    serializer_class = ExamListSerializer
    
    def post(self,*args,**kwargs):
        serializer = ExamStartSerializer(data =self.request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)             
        self.data =serializer.data
        return self.list(*args,**kwargs)

    def get_queryset(self):
        if Exam.has_user_active_exam(self.request.user):
            raise ParseError('a active exam alredy exist first close it')
        try:
            return Exam.start_random_exam(self.data["path"], 
                        user = self.request.user , level = self.data["level"] , 
                        source = self.data["source"] ,number = self.data["number"]  )
        except  ValidationError as e:
            raise ParseError(e.message)
        except  ObjectDoesNotExist :
            raise ParseError('matching lesson path does not exists')
        except ValueError:
            raise ParseError('number parametr must be digit')

        

class CheckHaveOpenExamMixin():
    def check_exam(self):        
        q = self.get_queryset()
        if not q.exists():
            raise NotFound('you have not any open Exam')
        return q
    
class UpdateExam(  CheckHaveOpenExamMixin,
                   generics.mixins.UpdateModelMixin,
                   generics.GenericAPIView ):
    
    def get_queryset(self):
        return Exam.objects.filter(user = self.request.user , is_active = True)
    def get_object(self):
        return Exam.objects.get(user = self.request.user , is_active = True)
        
    serializer_class = ExamSerializer

    def put(self,request,*args,**kwargs):
        self.check_exam()
        return super().update(request,*args,**kwargs)
    
    def patch(self,request,*args,**kwargs):
        self.check_exam()
        return super().patch(request,*args,**kwargs)
    
    
class FinishExam(CheckHaveOpenExamMixin ,generics.views.APIView ):
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

class ExamInfo(generics.RetrieveAPIView):#TODO: ExamStatistics
    serializer_class = ExamListSerializer
    
    def get_object(self):
        pk = self.kwargs.get('exam_id')
        if pk == 'active':
            return Exam.objects.get(user = self.request.user , is_active = True)
        
        if pk.isdigit():
            exam = Exam.objects.get(pk =pk)
            if exam.exists():
                if exam[0].user.pk == self.request.user.pk:
                    return exam
                raise NotAuthenticated('you cant access to this exam , this is not for you ')
    
        raise ParseError('uncorrect arguments')

class FullExamInfoView()