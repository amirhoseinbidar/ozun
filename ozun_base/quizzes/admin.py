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


# Register your models here.
admin.site.register(models.Quiz , QuizAdmin )
admin.site.register(models.Source)
admin.site.register(models.Answer)
admin.site.register(models.QuizStatus)
admin.site.register(models.Exam)
admin.site.register(models.ExamStatistic)
