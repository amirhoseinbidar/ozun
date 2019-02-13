# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics 
from restAPI.views import QuizSearchList
from restAPI.serializers import StudyPostSerializer , UserSerializer
from core.models import LessonTree
from users.models import User

class userProfileList(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        if pk.isdigit():
            return User.objects.filter(pk = pk)
        else:
            return User.objects.filter(username = pk)

class StudyPostList(generics.ListAPIView):
    serializer_class = StudyPostSerializer
    def get_queryset(self):
        return QuizSearchList.pathHandler(
                self.kwargs.get('LessonPath'))
    def get(self,request,*args,**kwargs):
        response = super(StudyPostList, self).get(request,*args,**kwargs)
        response.data['lesson'] = LessonTree.objects.get(
                pk = response.data['lesson']).full_path
        return response 