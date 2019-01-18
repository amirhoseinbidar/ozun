# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics 
from restAPI.views import QuizSearchList
from restAPI.serializers import StudyPostSerializer   
from course.models import LessonTree

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