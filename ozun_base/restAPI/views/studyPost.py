# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics , mixins , viewsets 
from studypost.models import  Magazine , Course
from ..serializers import MagazineSerializer , CourseSerializer , UserSerializer
from core.models import LessonTree 
from users.models import User
from ..utils import IsOwnerMixin ,LimitOffsetPaginationWrapper
from .base import GenericSearchView ,GenericFeedbackView

class userProfileList(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    def get_object(self):
        pk = self.kwargs['pk']
        if pk.isdigit():
            return User.objects.get(pk = pk)
        else:
            return User.objects.get(username = pk)

class MagazineViewSet( IsOwnerMixin,
                       viewsets.ModelViewSet ):

    serializer_class =  MagazineSerializer
    queryset = Magazine.objects.all()
    pagination_class = LimitOffsetPaginationWrapper(20)

class MagazineSearch(GenericSearchView):
    text_fields_search = ['title' , 'content']
    serializer_class = MagazineSerializer
    model = Magazine

class MagzineFeedback(GenericFeedbackView):
    model = Magazine


class CourseViewSet( IsOwnerMixin,
                     viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LimitOffsetPaginationWrapper(50)


class CourseSearch(GenericSearchView):
    text_fields_search = ['title' , 'content']
    serializer_class = CourseSerializer
    model = Course

class CourseFeedback(GenericFeedbackView):
    model =  Course