# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics , mixins , viewsets 
from studypost.models import  Magazine , Course
from ..serializers import MagazineSerializer , CourseSerializer , UserSerializer
from core.models import LessonTree 
from users.models import User
from ..utils import IsOwnerMixin ,LimitOffsetPaginationWrapper

class userProfileList(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        if pk.isdigit():
            return User.objects.filter(pk = pk)
        else:
            return User.objects.filter(username = pk)

class MagazineViewList(generics.ListAPIView):
    serializer_class = MagazineSerializer
    def get_queryset(self):
        #if self.kwargs['state'] == 'path':
        #   return Quiz.get_by_path(self.kwargs.get('LessonPath'))
        if self.kwargs['state'] == 'title':
            return Magazine.objects.filter(slug = self.kwargs['title'])

class MagazineViewSet( IsOwnerMixin,
                       viewsets.ModelViewSet ):
    
    serializer_class =  MagazineSerializer
    queryset = Magazine.objects.all()
    pagination_class = LimitOffsetPaginationWrapper(20)

class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    def get_queryset(self):
        ## TODO :: add a path
        #if self.kwargs['state'] == 'path':
        #    return Quiz.get_by_path(self.kwargs.get('LessonPath'))
        
        if self.kwargs['state'] == 'title':
            return Course.objects.filter(slug = self.kwargs['title'])
        

class CourseViewSet( IsOwnerMixin,
                     viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    #pagination_class = LimitOffsetPaginationWrapper(50)