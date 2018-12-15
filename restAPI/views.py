# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics  
from rest_framework.response import Response
from users.utils.emailAuth import sendAuthEmail
from .serializers import UserSerializer , User
from rest_framework import status
from .serializers import (QuizSerializer , Quiz , ProfileSerializer
    , Profile ,ExamSerializer , StudyPostSerializer  )
from django.http import Http404 
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from users.models import FeedBack
from quizzes.models import Exam,Source
from quizzes import utils
from django.db.models import Sum
from studylab.settings import TIME_ZONE
from core.utils import find_in_dict
from course.models import LessonTree
from rest_framework.exceptions import UnsupportedMediaType , ParseError , NotFound , NotAuthenticated

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
            raise ParseError(
                "unallowed action , allowed actions are 'most-voteds','lasts','path' ")

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
    def get(self,request,*args,**kwargs):
        response = super(ProfileView,self).get()
        return ProfileUpdate.response_maker(response)

class ProfileUpdate(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    

    def check_permissions(self,request):
        if request.content_type != 'application/json' :
            raise UnsupportedMediaType('','only "application/josn" content type accept')
            
              
        super(ProfileUpdate,self).check_permissions(request)
    
    def get_object(self):
        return Profile.objects.get(user = self.request.user)
    
    def request_maker(self):
        user = {'id' :self.request.user.id} 
       
        
        profile = Profile.objects.get(user = self.request.user)

        self.request.data['id'] = profile.id
        
        if 'last_name' in self.request.data:
            user['last_name'] = self.request.data.pop('last_name')
        if 'first_name' in self.request.data:
            user['first_name'] = self.request.data.pop('first_name')
        
        self.request.data['user'] = user
    
    @staticmethod
    def response_maker(response):
        data = response.data
        data.update( data.pop('user',None) or {} )
        return response

    def put(self,request,*args,**kwargs):
        self.request_maker()  
        print(self.request) 
        response = super(ProfileUpdate,self).put(self.request ,*args,**kwargs)
        return self.response_maker(response)

    def patch(self,*args,**kwargs):
        self.request_maker()
        response = super(ProfileUpdate,self).patch(*args,**kwargs)
        return self.response_maker(response)


        

class QuizFeedBack(generics.views.APIView):
    def post(self,request,pk):
        feedback_data = request.data.get('feedback_type',None)
        
        feedback_data = find_in_dict(feedback_data , FeedBack.FEEDBACK_TYPES)
        
        if not feedback_data:
            raise ParseError('uncorrect feedback')
        
        try:
            quiz = Quiz.objects.get(pk = pk)
        except ObjectDoesNotExist:
            raise ParseError('Quiz does not exist')
        
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
        data = self.request_orderer()
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
            raise ParseError('uncorrect level')
        if ('source' in data and 
                not Source.objects.filter(name =data['source']).exsits()):
            raise ParseError('source does not exits')
        if 'number' in data:
            if not data['number'].isdigit():
                raise ParseError('uncorrect number')
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
            raise NotFound('you have not any open Exam')
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
            raise NotAuthenticated('you cant access to this exam , this is not for you ')
        
        raise ParseError('uncorrect argomants')

class StudyPostList(generics.ListAPIView):
    serializer_class = StudyPostSerializer
    def get_queryset(self):
        return QuizSearchList.pathHandler(
                self.kwargs.get('LessonPath'))
    def get(self,request,*args,**kwargs):
        response = super(StudyPostList, self).get(request,*args,**kwargs)
        response.data['lesson'] = LessonTree.objects.get(
                pk = response.data['lesson']).turn_to_path()
        return response 