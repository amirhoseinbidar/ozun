# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from quizzes.models import Quizze
from django.contrib.auth.decorators import login_required
from django.http import Http404
from general_views.view import method_splitter
from random import randint
from django import forms
from quizzes.forms import  quiz_answers_form
from django.core.exceptions import ValidationError

def choice_without_repead(Queries,step=1):
    if not Queries or len(Queries) < step: 
        print('test')
        raise ValidationError('Queries must not empty or less then step')
    
    data =[]
    List = []  
    for record in Queries:
        List.append(record)    
    for _ in range(0,step):                         
        buf = randint(0,len(List)-1)
        data.append(List[buf])
        List.pop(buf) 
    
    return data

def str_to_dict(string,split_by):
    if not string:
        return Http404()
    string = string.replace(' ','')
    kwargs = {}

    for value in string.split(split_by):
        value = value.split('=')
        kwargs['{0}'.format(value[0])] = value[1]
    return kwargs

def make_ask_form(quizzes):    
    Forms =[]
    
    for quiz in quizzes:
        values = {}
        values['quiz'] = quiz.text
        list=quiz.answer.split('$$')# all answers store in a one string but every quistion seperate by this charecters
        answers_list =[]
        values['pk'] = quiz.pk
        i = 0
        for record in list:
            answer = {} 
            answer['answer']=record
            answer['number'] = i  
            answers_list.append(answer)
            i += 1
        values['answers'] = answers_list
        Forms.append(values)
    return Forms


def quizzes_ask(request,grade,lesson, chapter=None,topic=None,source=None,level=None):
      
    data = { 'topic__grade__pk':grade , 'topic__lesson__pk':lesson, }
    if chapter and chapter != '-1':
        data['topic__session__pk']=chapter
    if topic and topic != '-1':
        data['topic__pk']=topic
    if source and source != '-1':
        data['source__pk']=source
    if level and level != '-1':
        data['level__pk']=level

    quizzes = choice_without_repead( Quizze.objects.filter(**data),5)
    Forms = make_ask_form(quizzes)
    return render(request,'quizzes/quizzes_show.html',{'forms':Forms})






def quizzes_selector_POST(request):
    pass


def quizzes_ask_controller(request):
    data = {'request' : request}
    if ('grade' in request.GET and 'lesson' in request.GET 
        and request.GET['grade'] != '-1'and request.GET['lesson'] != '-1') :
        data['grade'] = request.GET['grade']
        data['lesson'] = request.GET['lesson']
    else:
        raise Http404() # GET request should have grade and lesson  argomant at least 

    if 'chapter' in request.GET:
        data['chapter'] = request.GET['chapter']
    if 'topic' in request.GET:
        data['topic'] = request.GET['topic']
    if 'source' in request.GET:
        data['source'] = request.GET['source']
    if 'level' in request.GET:
        data['level'] = request.GET['level']
    
    try:
        return quizzes_ask(**data)
    except Exception, e:
        raise ValidationError(e.message)

def quizzes_showAnswers_controller(request):
    if not request.POST:
        raise Http404()
    quizzes = []
    for name in request.POST:
        value = {}
        kwargs = str_to_dict(request.POST[name],'**')
        #make a dictionary with pk and number
        # number : specify that answer user choiced
        # pk  : specify that question user answered
        
        quiz = Quizze.objects.get(pk = kwargs['pk'])
        value['quiz'] = quiz.text
        answers = quiz.answer.split('$$')
        
        value['person_answer'] = answers[int(kwargs['number'])] 
        value['currect_answer'] = answers[quiz.currect_answer-1]
        value['is_answer_currect'] = int(kwargs('number')) == (quiz.currect_answer-1)
        value['advise'] = None #optional 
        value['exponential_answer'] = quiz.exponential_answer
        value['level'] =quiz.level
        value['grade'] = quiz.topic.grade.name
        value['lesson'] = quiz.topic.lesson.name
        value['chapter'] = quiz.topic.chapter.name
        value['topic'] = quiz.topic.name
        value['others'] = None # optional for other data like charts and helps

         
        
    

    

