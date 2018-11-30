# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint
from copy import deepcopy  
from json import dumps , loads

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import datetime
from django.db.models.query import QuerySet


def choice_without_repead(Queries,step=1):
    if not Queries:
        raise ValidationError('QuerySet not empty' ,code='empty query') 
    if Queries.count() < step: 
        raise ValidationError('the number of QuerySet members must not less then step',code='overflow step')
    
    data =[]
    List = list(Queries)   
    for _ in range(step):                         
        buf = randint(0,len(List)-1)
        data.append(List[buf])
        List.pop(buf) 
    
    return Queries.filter(pk__in = [item.pk for item in data])

def str_to_dict(string,split_by):
    '''for simple data trasfer it seperate every value by a special charecter(split_by) and covert it to dict'''
    if not string:
        return Http404()
    string = string.replace(' ','')
    kwargs = {}
    
    for value in string.split(split_by):
        value = value.split('=')
        kwargs['{0}'.format(value[0])] = value[1]
    return kwargs

def Score(quiz): 

    if quiz.quiz.correct_answer.pk != quiz.user_answer.pk :
        return -5
    if quiz.quiz.level == 'VE':
        return 1
    elif quiz.quiz.level == 'E':
        return 3
    elif quiz.quiz.level == 'M':
        return 5
    elif quiz.quiz.level == 'H':
        return 10
    elif quiz.quiz.level == 'VH':
        return 20
    
    raise Exception() # if level is no one of them so somthing is wrong 

from datetime import time
from django.utils.timezone import get_current_timezone 


def getTimeByLevel(level):
    from quizzes.models import Quiz

    if level == Quiz.VERY_EASY:
        return time(0,1,0)
    elif level == Quiz.EASY:
        return time(0,1,30) 
    elif level == Quiz.MEDIUM:
        return time(0,2,30) 
    elif level == Quiz.HARD:
        return time(0,5,0)
    elif level == Quiz.VERY_HARD:
        return time(0,10,0)
    
    raise ValidationError('unvalid level')





def make_ask_form(quizzes):    
    ''' 
        quizzes must be a query set of Quiz_status
    '''
    if not isinstance(quizzes , QuerySet):
        raise ValidationError('quizzes must be a query set of Quizzes_status')
    for quiz in quizzes:
        if not isinstance(quiz , Quiz_status):
            raise ValidationError('quizzes must be a query set of Quizzes_status')
    
    Forms = []
    for quiz_status in quizzes:
        values = {}
        values['quiz'] = quiz_status.quiz.text
        answers_list =[]
        values['pk'] = quiz_status.pk
        for record in quiz_status.quiz.quiz_answers.all():
            answer = { 'answer' : record.text, 'answer_pk' : record.pk}
            if record == quiz.user_answer:
                answer['checked'] = True 

            answers_list.append(answer)
        
        values['answers'] = answers_list
        Forms.append(values)
    return Forms



def make_answer_form(quizList):
    """ quizList is  a list or QuerySet of Quizzes status """
   
    context = {}
    buf = []
    context.update(calculate_score(quizList))
    for quiz in quizList:
        value = {}
        value['quiz'] = quiz.quiz.text
        value['person_answer'] = quiz.user_answer.text
        value['correct_answer'] = quiz.quiz.correct_answer.text
        value['is_answer_correct'] = quiz.user_answer.pk == quiz.quiz.correct_answer.pk
        
        if quiz.quiz.exponential_answer:
            value['exponential_answer'] = {#still optional
                'text':quiz.quiz.exponential_answer.text,
                'image':quiz.quiz.exponential_answer.image.url ,
                'video':quiz.quiz.exponential_answer.video.url,
            }
        value['level'] = quiz.quiz.level

        #value.update(quiz.quiz.get_all_topics())

        value['others'] = None # optional for other data like charts and helps
        
        buf.append(value)

    context['total_score'] = context['negative_score'] + context['positive_score']
    context['advise'] = None #optional
    context['quizzes'] = buf
    return context

def calculate_time(quizzes):
    ''' return '''
    time = 0 
    for quiz in quizzes:
        if  quiz.time_for_out:
            time += quiz.time_for_out.second
        else:
            time += getTimeByLevel(quiz.level).second
    return time

def calculate_score(quizList):
    negative_score = 0
    positive_score = 0
    for quiz in quizList:       
        score = Score(quiz = quiz)
        if score < 0 :
            negative_score += score
        else :
            positive_score += score
    return {'positive_score' : positive_score , 'negative_score' : negative_score}






def getAllQuizTests(user_pk):
    data = {'active_tests':[] , 'inactive_tests':[]}
    Tests = Quizzes_cash.objects.filter(name = 'quiz_page_token')
    for test in Tests:#TODO : this is not good way for do it 
        if int(loads(test.value)['user_pk']) == user_pk :
            if test.remove_date < datetime.now() or not test.is_active :
                users.utils.temporary_keys_cleaner.updateUserInfo(test)
            else:
                data['active_tests'].append({ 'end_time' : test.remove_date , 'token':test.key })
    

    Tests = UsersInfo.objects.filter(user__pk = user_pk)
    for test in Tests:
        data['inactive_tests'].append({ 'UsersInfoPk' : test.pk })


