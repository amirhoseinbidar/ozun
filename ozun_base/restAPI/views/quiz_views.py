# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics 
from restAPI.serializers import (
    QuizSerializer , Quiz ,ExamSerializer , 
    QuizStatusSerializer, QuizManagerSerializer ,
    SourceSerializer ,  LessonSeializer) 
from core.models import LessonTree
from rest_framework.exceptions import ParseError 
from core.exceptions import duplicationException
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from core.utils import find_in_dict
from core.models import FeedBack
from rest_framework.response import Response
from rest_framework import status
from json import dumps
from quizzes.models import Source
from users.models import User
from core.checks import APIExceptionHandler
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response



class QuizPagination(LimitOffsetPagination):
    default_limit = 10

class SourcePagination(LimitOffsetPagination):
    default_limit = 50

class QuizSearchList(APIExceptionHandler, generics.ListAPIView): # need test
    allowed_actions = ['most-voteds','lasts','path']
    pagination_class = QuizPagination
    serializer_class = QuizSerializer
    
    def get_queryset(self):
        action = self.kwargs['action'] 
        if not action in self.allowed_actions:
            raise ParseError(
                "unallowed action , allowed actions are {} ".format(self.allowed_actions))
       
        elif action == 'most-voteds': 
            return self.most_votedsHandler(**self.kwargs)
        elif action == "lasts":
            return self.lastsHandler(**self.kwargs)
        elif action == 'path':
            return self.pathHandler(self.kwargs.get('LessonPath'))

    
    def most_votedsHandler(self,**kwargs):
        return Quiz.get_mostVotes()

    def lastsHandler(self,**kwargs):
        return Quiz.objects.all()
  
    def pathHandler(self ,LessonPath):
        try:
            return Quiz.get_by_path(LessonPath)
        except ObjectDoesNotExist:
            raise ParseError('matching lesson path does not exist')

        
class QuizFeedBack(generics.views.APIView):
    def post(self,request,quiz_pk):
        feedback_data = request.data.get('feedback_type',None)
        feedback_data = find_in_dict(feedback_data , FeedBack.FEEDBACK_TYPES)
        
        if not feedback_data:
            raise ParseError('uncorrect feedback')
        
        try:
            quiz = Quiz.objects.get(pk = quiz_pk)
        except ObjectDoesNotExist:
            raise ParseError('Quiz does not exist')
        
        try:# if user voted before , update it
            feedback = quiz.votes.get(user = request.user)
        except ObjectDoesNotExist:# if not create new 
            feedback = FeedBack(user = request.user, content_object = quiz) 

        feedback.feedback_type = feedback_data
        feedback.save()
        quiz.count_votes()
     
        return Response(data = 'quiz voted' , status = status.HTTP_200_OK)


class QuizCreate(generics.CreateAPIView):
    serializer_class = QuizManagerSerializer

    def post(self,*args,**kwargs):
        # if 'added_by' is not exists let this go on parent method will raise error
        user_pk = self.request.data.get('added_by' , None)
        if user_pk and str(user_pk).isdigit :
            if  self.request.user != User.objects.get(pk = user_pk):
                raise ParseError('you can not create quiz as another user')
        return super().post(*args,**kwargs)


class QuizUpdate(generics.UpdateAPIView):
    serializer_class = QuizManagerSerializer
    def get_queryset(self): 
        return Quiz.objects.filter(added_by = self.request.user)
    
    def put(self ,*args,**kwargs):
        user_pk = self.request.data.get('added_by' , None)
        if user_pk and str(user_pk).isdigit :
            if  self.request.user != User.objects.get(pk = user_pk):
                raise ParseError('you can not create quiz as another user')
        return super().put(*args,**kwargs)

    def patch(self,*args,**kwargs):
        user_pk = self.request.data.get('added_by' , None)
        if user_pk and str(user_pk).isdigit :
            if  self.request.user != User.objects.get(pk = user_pk):
                raise ParseError('you can not create quiz as another user')
        return super().patch(*args,**kwargs)
        

class LessonPathView(generics.GenericAPIView):
    def post(self , request):
        if 'path' in self.request.data:
            path = self.request.data['path']
        else:
            raise ParseError('path is required')
        
    
        if path == 'root':
            objs = LessonTree.get_root_nodes() 
        else:
            try :
                objs = LessonTree.find_by_path(path).get_children()
               
            except ObjectDoesNotExist:
                raise ParseError('uncorrect path')
        
        return Response( LessonSeializer(objs , many=True).data )

class SourceView(generics.ListAPIView):
    serializer_class = SourceSerializer
    pagination_class = SourcePagination
    def get_queryset(self):
        return Source.objects.all()
            
