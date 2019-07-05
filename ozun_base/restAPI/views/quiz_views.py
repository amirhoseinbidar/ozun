# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics , mixins , viewsets 
from restAPI.serializers import ( 
    QuizStatusSerializer, QuizManagerSerializer ,
    SourceSerializer ,   Quiz  , LessonSeializer
) 
from core.models import LessonTree
from rest_framework.exceptions import ParseError 
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from core.models import FeedBack
from quizzes.models import Source
from core.checks import APIExceptionHandler
from rest_framework.response import Response
from ..utils import IsOwnerMixin , LimitOffsetPaginationWrapper
from .base import (
    GenericFeedbackView , 
    UP_VOTE , DOWN_VOTE ,
    GenericSearchView ,
)

class QuizMostVote(generics.ListAPIView): 
    pagination_class = LimitOffsetPaginationWrapper()
    serializer_class = QuizManagerSerializer

    def get_queryset(self):
        return Quiz.get_mostVotes()

        

class QuizSearchContent(GenericSearchView):
    model = Quiz
    serializer_class = QuizManagerSerializer
    text_fields_search = ['exponential_answer' , 'content']

        
class QuizFeedBack(GenericFeedbackView):
    model = Quiz
    allow_feedbacks = [UP_VOTE,DOWN_VOTE]


class LessonPathView(generics.GenericAPIView):
    pagination_class = LimitOffsetPaginationWrapper(10)
    def post(self , request):
        if 'path' in self.request.data:
            path = self.request.data['path']
        else:
            raise ParseError('path is required')
        
        if path == '/':
            objs = LessonTree.get_root_nodes() 
        else:
            try :
                objs = LessonTree.find_by_path(path).get_children()
            except ObjectDoesNotExist:
                raise ParseError('uncorrect path')
        
        return Response( LessonSeializer(objs , many=True).data )

class QuizManagerViewSet(IsOwnerMixin , viewsets.ModelViewSet ):
    serializer_class = QuizManagerSerializer 
    pagination_class = LimitOffsetPaginationWrapper()
    def get_queryset(self):
        return Quiz.objects.all()

class SourceView(generics.ListAPIView):
    serializer_class = SourceSerializer
    pagination_class = LimitOffsetPaginationWrapper(50)
    def get_queryset(self):
        return Source.objects.all()
            
