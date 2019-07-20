# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import choice
from copy import deepcopy
from json import dumps, loads
from datetime import datetime, time

from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import get_current_timezone


def choice_without_repead(Queries, step=1, check_step_oveflow=True):
    if not Queries or Queries.count() == 0:
        raise ValidationError('QuerySet is empty', code='empty_query')

    length = Queries.count()

    if Queries.count() < step:
        if check_step_oveflow:
            raise ValidationError(
                'the number of QuerySet members must not less then step', code='step_overflow')
        else:
            step = length

    data = list(range(length))
    pks = []
    for _ in range(step):
        ch = choice( data )
        i = data.index(ch)
        data.pop(i)
        pks.append(Queries[ch].pk)

    return Queries.filter(pk__in = pks )


def Score(quiz_status):

    answer_pk = quiz_status.quiz.answer_set.get(is_correct_answer=True).pk
    level = quiz_status.quiz.level 
    if (not quiz_status.user_answer or quiz_status.user_answer.pk != answer_pk ):
        return -5
    if level == 'VE':
        return 1
    elif level == 'E':
        return 3
    elif level == 'M':
        return 5
    elif level == 'H':
        return 10
    elif level == 'VH':
        return 20

    raise Exception("UNCORRECT LEVEL")  # if level is no one of them so somthing is wrong


def getTimeByLevel(level):
    from quizzes.models import Quiz

    if level == Quiz.VERY_EASY:
        return time(0, 1, 0)
    elif level == Quiz.EASY:
        return time(0, 1, 30)
    elif level == Quiz.MEDIUM:
        return time(0, 2, 30)
    elif level == Quiz.HARD:
        return time(0, 5, 0)
    elif level == Quiz.VERY_HARD:
        return time(0, 10, 0)

    raise ValidationError('unvalid level')


def calculate_time(quizzes):
    ''' return '''
    time = 0
    for quiz in quizzes:
        if quiz.time_for_out:
            time += quiz.time_for_out.second
        else:
            time += getTimeByLevel(quiz.level).second
    return time


def calculate_score(quizList):
    negative_score = 0
    positive_score = 0
    for quiz in quizList:
        score = Score(quiz)
        if score < 0:
            negative_score += -(score)
        else:
            positive_score += score
    return (positive_score, negative_score)


def turn_second_to_time(second):
    second = int(second)
    hour = (second//3600)
    minute = (second - hour*3600)//60
    second = second - (hour*3600 + minute*60)
    return time(hour=hour, minute=minute, second=second)
