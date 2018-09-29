# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models

class quizzesAdmin(admin.ModelAdmin):
    filter_horizontal = ('quiz_answers','topics',)
    raw_id_fields = ('correct_answer',)
    readonly_fields = ['added_by']
    def address(self,obj):
        base = '{}/{}'.format(obj.grade.name , obj.lesson.name)
        data = ''
        if not obj.topics.all().exists():
            return base
        for topic in obj.topics.all():
            data += base+'/{}/{} \n '.format(topic.chapter.name ,topic.name)
        
        return data

    list_display = ('level','timeOut','address')
class topicAdmin(admin.ModelAdmin):
    filter_horizontal = ('grades',)
class chapterAdmin(admin.ModelAdmin):
    filter_horizontal = ('grades',)
class lessonAdmin(admin.ModelAdmin):
    filter_horizontal = ('grades',)

class QuizzesAdminSite(admin.AdminSite):
    site_header = "StudyLab Quizzes Admin"
    site_title = 'StudyLab Quizzes Admin Portal'
    index_title = 'Welome to Quizzes Administration Portal'
quizzesAdminSite = QuizzesAdminSite(name='quizzes_admin')

# Register your models here.
quizzesAdminSite.register(models.Quizzes,quizzesAdmin)
quizzesAdminSite.register(models.Source)
quizzesAdminSite.register(models.Grade)
quizzesAdminSite.register(models.Lesson , lessonAdmin)
quizzesAdminSite.register(models.Topic , topicAdmin)
quizzesAdminSite.register(models.Chapter , chapterAdmin)
quizzesAdminSite.register(models.Exponential_answer)
quizzesAdminSite.register(models.Answers)
quizzesAdminSite.register(models.Quizzes_status)

