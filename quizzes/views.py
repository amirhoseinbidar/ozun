# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render , redirect 
from quizzes.models import Quiz,Answer
from django.contrib.auth.decorators import login_required
from django.http import Http404 , JsonResponse
from generics.view import method_splitter
from django import forms
from django.core.exceptions import ValidationError , ObjectDoesNotExist
from datetime import datetime
from .utils import (
    make_ask_form , getTimeByLevel ,calculate_time ,choice_without_repead,
    str_to_dict ,Score  ,make_answer_form )
from quizzes.models import Exam
from json import dumps , loads
from django.utils import timezone
from copy import deepcopy
from studylab.settings import TIME_ZONE


def quizzes_ask(request,token,grade,lesson, chapter=None,topic=None,source=None,level=None):
    try:
        key = QuizzesInfo.objects.get(key= token) #just one key should be
    except ObjectDoesNotExist:
        key = None
    
    if key: # is exist
        if key.is_active:
            if key.isOutOfDate():
                key.disable()
                return redirect('/accounts/profile')
            if key.user != request.user: # just a little authenticate test
                return redirect('/accounts/profile')
    
            Forms = make_ask_form(key.quizzes_status.all())

        else:
            return redirect('/accounts/profile')
    
    else:
        data = { 'grade__pk':grade ,
             'lesson__pk':lesson, }
        if chapter and chapter != '-1':
            data['topic__chapter__pk']=chapter
        if topic and topic != '-1':
            data['topic__pk']=topic
        if source and source != '-1':
            data['source__pk']=source
        if level and level != '-1':
            data['level']=level
        try :
            quizzes = choice_without_repead( Quizzes.objects.filter(**data),4)
        except ValidationError:
            if e.code == 'empty query':
                return JsonResponse({'error':'you send uncorrect data or there is not any quiz for your request'})
                
            if e.code == 'overflow step':
                return JsonResponse({'error':'apologize , quizzes is not enough for servies'})
            else :
                return JsonResponse({'error':e.message })
        
        quizzes_status = Quizzes_status.saveFromQuizzesSet(quizzes)
        Forms = make_ask_form( quizzes_status )
        timeout = calculate_time(quizzes)
        
        key_value = {'user_pk' : request.user.pk , 'quizzes' : [] }
        for quiz in quizzes:
            key_value['quizzes'].append({'quiz_pk': quiz.pk ,'answer_number': -1 })
       
        key =  QuizzesInfo().create_record(key = token, user = request.user ,
                    quizzes_status = quizzes_status , forward_time=timeout)
        
        #quizzes is just quizzes they dont have user answers this method of quizzes_status make
        #quizzes_status with user_answer = None  from a set of quizzes
    
    return render(request,'quizzes/ask.xhtml',{'forms':Forms,'token': token , 'timeout':key.close_date ,'tome_zone':TIME_ZONE  })

@login_required
def quizzes_ask_controller(request):
    data = {'request' : request} 
    
    
    if 'token' in request.POST:
        data['token'] = request.POST['token']
    else:
       return redirect('/accounts/profile')
        
    if 'lesson' in request.POST and 'grade' in request.POST: # lesson and grade should be together 
        data['lesson'] = request.POST['lesson']
        data['grade'] = request.POST['grade']

    if 'chapter' in request.POST:# this requests is optional user can dont use this options
        data['chapter'] = request.POST['chapter']
    if 'topic' in request.POST:
        data['topic'] = request.POST['topic']
    if 'source' in request.POST:
        data['source'] = request.POST['source']
    if 'level' in request.POST:
        data['level'] = request.POST['level']
    
    return quizzes_ask(**data)
    

# data send to this method like it  
# request['answer_""quiz_status_pk"" '] ={quiz_status_pk:## ,answer_pk:##} , request['answer_""quiz_status_pk"" '] ={quiz_status_pk:## , answer_pk:##} ,...
@login_required
def quizzes_showAnswers_controller(request):
    if not request.POST or not 'token' in request.POST:
        return redirect('/accounts/profile')
    try:
        key = QuizzesInfo.objects.get(key= request.POST['token'])
    except ObjectDoesNotExist:
        key = None

    if not key or not key.is_active :
        return redirect('/accounts/profile')
    key.disable()
    
    quizList = []
    quizDict = deepcopy(request.POST)
    quizDict.pop('csrfmiddlewaretoken' , None)
    quizDict.pop('token' , None)
    
    for k in quizDict:
        try:
            data = loads(quizDict[k]) #data send in json format in template we regulate it  
        except: #any exception so something wrong and some one want send uncorrect data 
            return JsonResponse({'error': 'uncorrect data'})
        quizList.append(data) 
    
    try:
        __quizList = Quizzes_status.saveFromDictList(quizList) 
    except :
         return JsonResponse({'error': 'unallowed data'})
    
    context = make_answer_form(__quizList)

    return render(request,'quizzes/answer.xhtml',context) 
   
def showAnswerByUserInfo():
    pass

@login_required
def UpdateQuizzesInfo(request):
    try:
        key = QuizzesInfo.objects.get(key= request.POST['token'])
        if key.isOutOfDate():
            key.disable()
            raise ObjectDoesNotExist()
    except ObjectDoesNotExist:
        key = None
    if not key :  
        return JsonResponse({'error': 'uncorrect token'})      
    
    try :#data should be number it protect our code from other data type problems
         data = loads(request.POST['data']) 
    except :
        return JsonResponse({'error': 'uncorrect data'})
    
    
    if key.user.pk != request.user.pk:
        return JsonResponse({'error': 'you are not allowing change data'})
    try:
        quiz = key.quizzes_status.get(pk = data['quiz_status_pk'])
    except ObjectDoesNotExist:
        quiz = None

    if quiz:#if there was a quiz with same pk , turn its user_answer to new answer 
        if quiz.user_answer:
            prev_pk = quiz.user_answer.pk
            quiz.user_answer.pk = data['answer_pk']
            quiz.save()
            key.save()
            return JsonResponse({
                'message':'quiz {0} from user {1} status : answer from id {2} turn to id {3}'.format(
                    quiz.quiz.pk , key.user.pk , prev_pk , quiz.user_answer.pk   
                )})
        
        quiz.user_answer = Answers.objects.get(pk = data['answer_pk'])
        quiz.save()
        key.save()
        return JsonResponse({
            'message':'answer {} record for user {} as the answer of quiz {} '.format(
                quiz.user_answer.pk , key.user.pk , quiz.quiz.pk

            )
        })

            

    
    #if not so something wrong becouse we cashed all allow quizzes  
    return JsonResponse({'error':'unallowed data'})

    

    

