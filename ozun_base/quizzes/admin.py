# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models
from django import forms
from quizzes.models import Quiz, Answer
from json import dumps, loads
from django.core.exceptions import ValidationError

class AnswerInline(admin.StackedInline):
    model = Answer

class QuizAdmin(admin.ModelAdmin):
    search_fields = ['content' , 'exponential_answer']
    inlines = [AnswerInline ,]

class QuizzesAdminSite(admin.AdminSite):
    site_header = "ozun Quizzes Admin"
    site_title = 'ozun Quizzes Admin'
    index_title = 'Welome to Quizzes Administration'


quizzesAdminSite = QuizzesAdminSite(name='quizzes_admin')

# Register your models here.
quizzesAdminSite.register(models.Quiz , QuizAdmin )
quizzesAdminSite.register(models.Source)
quizzesAdminSite.register(models.Answer)
quizzesAdminSite.register(models.QuizStatus)
quizzesAdminSite.register(models.Exam)
quizzesAdminSite.register(models.ExamStatistic)
