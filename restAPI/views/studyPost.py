# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics 
from quizzes.models import Quiz
from restAPI.serializers import magazineSerializer , CourseSerializer , UserSerializer
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
    serializer_class = magazineSerializer
    def get_queryset(self):
        return Quiz.get_by_path(self.kwargs.get('LessonPath'))

class StudyPostList(generics.ListAPIView):
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Quiz.get_by_path(self.kwargs.get('LessonPath'))