# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render , redirect 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from quizzes.models import Exam , ExamStatistic
from django.views.generic import DetailView
from core.exceptions import duplicationException
from django.contrib.auth.mixins import LoginRequiredMixin

class ExamView(LoginRequiredMixin , DetailView):
    model = Exam
    template_name = 'quizzes/ask.xhtml'

    def get_object(self):
        print(self.request.GET)
        print(self.request.query_params)
        try:
            return Exam.start_random_exam(  
                self.kwargs['LessonPath'] ,
                self.request.user
            )
        except duplicationException:
            return Exam.objects.filter(
                user = self.request.user,
                is_active = True 
            )



class ExamInformationView(LoginRequiredMixin,DetailView):
    model = Exam

    def get_object(self):
        exam = Exam.objects.filter(pk = self.kwargs['pk'])
        if exam.user.pk == self.request.user.pk:
            return ExamStatistic.object.filter(exam__pk = self.kwargs['pk'])
    
        raise Http404

###### 
# exam updating and finishing perform with jquery and ajax they
# request to rest_api urls to do this so there is no need to make 
# any form for update exam  
######
    

    

