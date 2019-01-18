# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics 
from restAPI.serializers import  Quiz , ExamSerializer,ExamListSerializer , QuizStatusSerializer  
from quizzes.models import Exam,Source
from quizzes import utils
from . import QuizSearchList
from core.exceptions import duplicationException
from rest_framework.exceptions import UnsupportedMediaType , NotFound , ParseError , NotAuthenticated ,APIException
from core.utils import find_in_dict
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


class StartExam(generics.ListAPIView):
    
    serializer_class = ExamListSerializer
    
    def get_queryset(self):
        data = self.request_orderer()
        number = data.pop('number')
        print(data)
        quizzes = QuizSearchList.pathHandler(
            self.kwargs.get('LessonPath')).filter(**data)

        quizzes = utils.choice_without_repead(quizzes,number,False)
        try:
            exam = Exam.create_exam(quizzes,self.request.user)
        except duplicationException as e:
            raise ParseError(e,400)

        return Exam.objects.filter(pk = exam.pk)
    
    def request_orderer(self): # check optional argumants 
        data = dict(self.request.query_params.copy())
        
        if 'level' in data : 
            data['level'] = data['level'][0]
            
            if not find_in_dict(data['level'], Quiz.LEVEL_TYPE):
                raise ParseError('uncorrect level')
            
            data['level'] = dict(Quiz.REVERS_LEVEL_TYPE)[data['level']]

        if 'source' in data :
            data['source'] = data['source'][0]
            try:
                data['source'] = Source.objects.get(name =data['source']).pk
            except ObjectDoesNotExist:
                raise ParseError('source does not exits')
        
        if 'number' in data:    
            data['number'] = data['number'][0]
            if not data['number'].isdigit():
                raise ParseError('uncorrect number')
            data['number'] = int(data['number'])
        
        else:
            data['number'] = 15
        
        return data


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
            #TODO: ExamStatistics 
        }
        return Response(data , status.HTTP_200_OK )

class ExamInfo(generics.ListAPIView):
    
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
