# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics  
from rest_framework.response import Response
from users.utils.emailAuth import sendAuthEmail
from .serializers import UserSerializer , User
from rest_framework import status
from quizzes.models import Quiz
from django.http import Http404


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

class QuizSearchList(generics.ListAPIView):
    allowed_actions = ['most-voteds','lasts']
    def get_queryset(self,request,action):
        if not action in self.allowed_actions:
            return Http404

        if not 'From' in request.data:
            if action == "most-voteds":
                self.queryset = Quiz.get_mostVotes(1,50)
            elif action == "lasts":
                self.queryset = Quiz.objects.all[:50]#Quizzes orderd by Time in default
            return
        
        From = request.data.get('From')
        To = request.data.get('To')
        if action == "most-voteds":    
            self.queryset = Quiz.get_mostVotes(From,To)
        elif action == "lasts":
            self.queryset = Quiz.objects.all[From:To]
        


        
