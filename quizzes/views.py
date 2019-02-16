# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render , redirect 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from quizzes.models import Exam , ExamStatistic
from django.views.generic import DetailView
from core.exceptions import duplicationException
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import examStartForm

class ExamView(LoginRequiredMixin , DetailView):
    model = Exam
    template_name = 'quizzes/ask.html'
    opt_data = None

    def get_object(self):
        if self.kwargs.pop('is_post' ,False):
            return Exam.start_random_exam(  
                self.kwargs['LessonPath'] ,
                self.request.user,
                **self.opt_data)
        else :
            exam = Exam.objects.filter(
                user = self.request.user,
                is_active = True )
            if not exam.exists():
                raise Http404()
            return exam
        
    def post(self,*args,**kwargs):
        form = examStartForm(self.request.POST)
        if form.is_valid():
            self.kwargs['LessonPath'] = form.get_lesson_path()
            self.kwargs['is_post'] = True
            self.get_optional_data({
                'level' : form['level'].value(),
                'source' : form['source'].value(),
                'number' : form['number'].value(),
            })
            return self.get(self.request)

    def get_optional_data(self,dic):
        data = {}
        if dic['level']:
            data['level'] = dic['level']
        if dic['source']:
            data['source'] = dic['source']
        if dic['number']:
            data['number'] = int(dic['number'])
        print(dic)
        self.opt_data = data
            
        



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
    

    

