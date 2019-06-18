# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from random import randint
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

    if check_step_oveflow:
        if Queries.count() < step:
            raise ValidationError(
                'the number of QuerySet members must not less then step', code='step_overflow')
    else:
        if Queries.count() < step:
            step = Queries.count()

    data = []
    List = list(Queries)
    for _ in range(step):
        buf = randint(0, len(List)-1)
        data.append(List[buf])
        List.pop(buf)

    return Queries.filter(pk__in=[item.pk for item in data])


def Score(quiz_status):
    if (not quiz_status.user_answer or
            quiz_status.quiz.answer_set.get(is_correct_answer=True).pk
            != quiz_status.user_answer.pk):
        return -5
    if quiz_status.quiz.level == 'VE':
        return 1
    elif quiz_status.quiz.level == 'E':
        return 3
    elif quiz_status.quiz.level == 'M':
        return 5
    elif quiz_status.quiz.level == 'H':
        return 10
    elif quiz_status.quiz.level == 'VH':
        return 20

    raise Exception()  # if level is no one of them so somthing is wrong


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
