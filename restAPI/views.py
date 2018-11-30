# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics  
from rest_framework.response import Response
from users.utils.emailAuth import sendAuthEmail
from .serializers import UserSerializer , User
from rest_framework import status
from .serializers import (QuizSerializer , Quiz , ProfileSerializer
    , Profile ,ExamSerializer  )
from django.http import Http404 
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from users.models import FeedBack
from quizzes.models import Exam,Source
from quizzes import utils
from django.db.models import Sum
from studylab.settings import TIME_ZONE
from core.models import LessonTree
from core.utils import find_in_dict

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    def post(self,request):
        response = super(UserCreate,self).post(request)
        
        username = request.data.get('username')
        email = request.data.get('email')
        
        user = User.objects.get(username = username)
        user.is_active  = False
        user.save()
        
        sendAuthEmail(request,user,email)
        response.data['notification'] = "a Authonticate email send to %s please open email and click on link for complete progress" %(email)
        
        return response

class QuizSearchList(generics.ListAPIView): # need test
    allowed_actions = ['most-voteds','lasts','path']
    serializer_class = QuizSerializer
    def get_queryset(self):
        action = self.kwargs['action']
        if not action in self.allowed_actions:
            raise Http404

        elif action == 'most-voteds':
            return self.most_votedsHandler(**self.kwargs)
        elif action == "lasts":
            return self.lastsHandler(**self.kwargs)
        elif action == 'path':
            return self.pathHandler(self.kwargs.get('LessonPath'))
           
    
    def most_votedsHandler(self,**kwargs):
        if not 'From' in kwargs:
            return Quiz.get_mostVotes(1,50)
         
        From = kwargs.get('From')
        To = kwargs.get('To')  
        return Quiz.get_mostVotes(From,To)

    def lastsHandler(self,**kwargs):
        if not 'From' in kwargs:
            return Quiz.objects.all()[:50]#Quizzes orderd by Time in default
        
        From = kwargs.get('From')
        To = kwargs.get('To')
        return Quiz.objects.all()[From:To]
    
    #NOTE:it should send quizzes by given path I think TreeBeard have some tools
    # and second is its url give every thing this is unsafe
    @staticmethod
    def pathHandler(LessonPath):
        branch = LessonTree.find_by_path(LessonPath)
        quizzes =Quiz.objects.filter( 
            lesson__in = list(branch.get_descendants()) )

        return quizzes

class ProfileView(generics.ListAPIView):
    serializer_class= ProfileSerializer
    def get_queryset(self):
        return Profile.objects.filter(pk = self.kwargs['pk'])
    
class ProfileUpdate(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    
    def get_object(self):
        return Profile.objects.get(user = self.request.user)

    def put(self,request,*args,**kwargs):
        data = dict(request.data)
        if 'user' in data:
            user_ser = UserSerializer(self.request.user ,  data['user'])
            del data['user']
        profile = Profile.objects.get(user = self.request.user)
       
        response = super(ProfileUpdate,self).put(
            request = request , pk = profile.pk)
        
        if user_ser.is_valid():# it is better to do it in serializer itself
            user_ser.save()
            response.data['user'] = user_ser.data
            return response

        response.data['error'] = user_ser.errors
        return response
        
    def patch(self,*args,**kwargs):
        response = super(ProfileUpdate,self).patch(*args,**kwargs)
        user = UserSerializer(self.request.user)
        response.data['user'] = user.data
        return response


        

class QuizFeedBack(generics.views.APIView):
    def post(self,request,pk):
        feedback_data = request.data.get('feedback_type',None)
        
        feedback_data = find_in_dict(feedback_data , FeedBack.FEEDBACK_TYPES)
        
        if not feedback_data:
            return Response(data='uncorrect feedback' 
                , status = status.HTTP_400_BAD_REQUEST)
        
        try:
            quiz = Quiz.objects.get(pk = pk)
        except ObjectDoesNotExist:
            return Response(data = 'Quiz does not exist' ,
                status = status.HTTP_400_BAD_REQUEST)
        
        try:# if user voted , update it
            feedback = quiz.votes.get(user = request.user)
        except ObjectDoesNotExist:# if not create new 
            feedback = FeedBack(user = request.user, content_object = quiz) 

        feedback.feedback_type = feedback_data
        feedback.save()
     
        return Response(data = 'quiz voted' , status = status.HTTP_200_OK)

class StartExam(generics.ListAPIView):
    serializer_class = QuizSerializer
    exam = None
    def get_queryset(self):
        
        try:
            data = self.request_orderer()
        except ValidationError,e: #NOTE: it is deffrent in py3
            return Response(data = e.message , status=status.HTTP_400_BAD_REQUEST)
        number = data.pop('number')
        
        quizzes = QuizSearchList.pathHandler(
            self.kwargs.get('LessonPath')).filter(**data)

        quizzes = utils.choice_without_repead(quizzes,number)
        self.exam = Exam.create_exam(quizzes,self.request.user)
        return quizzes
    
    def request_orderer(self): # check optional argumants 
        data = self.request.data.copy()
        if ('level' in data and 
                not find_in_dict(data['level'] , Quiz.LEVEL_TYPE)):
            raise ValidationError('uncorrect level')
        if ('source' in data and 
                not Source.objects.filter(name =data['source']).exsits()):
            raise ValidationError('source does not exits')
        if 'number' in data:
            if not data['number'].isdigit():
                raise ValidationError('uncorrect number')
            data['number'] = int(data['number'])
        else:
            data['number'] = 15
        
        return data

            
    def get(self,*args,**kwargs):
        response = super(StartExam,self).get(*args,**kwargs)
        response.data['finish_time'] = self.exam.close_date
        response.data['exam_id'] = self.exam.pk
        response.data['time_zone'] = TIME_ZONE
        return response

class UpdateExam(generics.UpdateAPIView):
    serializer_class = ExamSerializer
    exam = None
    def put(self,request,*args,**kwargs):
        try:
            self.exam = Exam.objects.get(user = self.user , is_active = True)
        except ObjectDoesNotExist:
            return Response('you have not any open Exam' , status.HTTP_404_NOT_FOUND)
        return super(UpdateExam,self).put(request,pk = self.exam.pk 
            , *args,**kwargs)

class FinishExam(UpdateExam):#just like update exam but after update close exam 
    def put(self,request,*args,**kwargs):
        response = super(FinishExam,self).put(*args,**kwargs)
        self.exam.disable()
        return response

class ExamInfo(generics.ListAPIView):
    serializer_class = ExamSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk == 'active':
            return Exam.objects.get(is_active = True)
        if pk.isdigit():
            exam = Exam.objects.get(pk =pk)
            if exam.user.pk == self.request.pk:
                return exam
            raise ValidationError('you cant access to this exam , this is not for you ')
        
        raise ValidationError('uncorrect argomants')