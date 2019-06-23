# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models
from django import forms
from quizzes.models import Quiz, Answer
from json import dumps, loads
from django.core.exceptions import ValidationError


class quizAdminRules(admin.ModelAdmin):

    def get_queryset(self, request):
        queryset = super(quizAdminRules, self).get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(added_by=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super(quizAdminRules, self).save_model(request, obj, form, change)

class AnswerAdmin(admin.StackedInline):
    model = Answer

class QuizAdmin(quizAdminRules):
    inlines = [ AnswerAdmin, ]

class topicAdmin(quizAdminRules):
    filter_horizontal = ('grades',)
    readonly_fields = ['added_by']


class chapterAdmin(quizAdminRules):
    filter_horizontal = ('grades',)
    readonly_fields = ['added_by']


class lessonAdmin(quizAdminRules):
    filter_horizontal = ('grades',)
    readonly_fields = ['added_by']


class QuizzesAdminSite(admin.AdminSite):
    site_header = "ozun Quizzes Admin"
    site_title = 'ozun Quizzes Admin Portal'
    index_title = 'Welome to Quizzes Administration Portal'


quizzesAdminSite = QuizzesAdminSite(name='quizzes_admin')

# Register your models here.
quizzesAdminSite.register(models.Quiz, QuizAdmin)
quizzesAdminSite.register(models.Source)
quizzesAdminSite.register(models.Answer)
quizzesAdminSite.register(models.QuizStatus)
quizzesAdminSite.register(models.Exam)
quizzesAdminSite.register(models.ExamStatistic)
