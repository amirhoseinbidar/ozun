# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics 
from restAPI.serializers import QuizSerializer , Quiz ,ExamSerializer , StudyPostSerializer , QuizStatusSerializer  
from rest_framework.exceptions import ParseError 
from course.models import LessonTree
from core.exceptions import duplicationException
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from core.utils import find_in_dict
from users.models import FeedBack
from rest_framework.response import Response
from rest_framework import status

class QuizSearchList(generics.ListAPIView): # need test
    allowed_actions = ['most-voteds','lasts','path']
    serializer_class = QuizSerializer
    def get_queryset(self):
        action = self.kwargs['action'] 
        if not action in self.allowed_actions:
            raise ParseError(
                "unallowed action , allowed actions are 'most-voteds','lasts','path' ")

        elif action == 'most-voteds':
            return self.most_votedsHandler(**self.kwargs)
        elif action == "lasts":
            return self.lastsHandler(**self.kwargs)
        elif action == 'path':
            return self.pathHandler(self.kwargs.get('LessonPath'))
           
    
    def most_votedsHandler(self,**kwargs):
        if not ('from' in kwargs and 'to' in kwargs):
            return Quiz.get_mostVotes(1,50)
         
        From = int(kwargs.get('from'))
        To = int(kwargs.get('to'))  
        return Quiz.get_mostVotes(From,To)

    def lastsHandler(self,**kwargs):#code duplicate with line 60
        if not ('from' in kwargs and 'to' in kwargs):
            return Quiz.objects.all()[:50]#Quizzes orderd by Time in default
        
        From = int(kwargs.get('from'))
        To = int(kwargs.get('to'))
        return Quiz.objects.all()[From:To]
  
    @staticmethod
    def pathHandler(LessonPath):
        return Quiz.get_by_path(LessonPath)
            
        


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
     
        return Response(data = 'quiz voted' , status = status.HTTP_200_OK)
