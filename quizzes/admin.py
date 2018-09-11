# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models

class quizzesAdmin(admin.ModelAdmin):
    #filter_horizontal = ('quiz_answers','topics',)
    raw_id_fields = ('correct_answer',)
class topicAdmin(admin.ModelAdmin):
    filter_horizontal = ('grade',)
class chapterAdmin(admin.ModelAdmin):
    filter_horizontal = ('grade',)
class lessonAdmin(admin.ModelAdmin):
    filter_horizontal = ('grade',)
    
# Register your models here.
admin.site.register(models.Quizzes,quizzesAdmin)
admin.site.register(models.Source)
admin.site.register(models.Grade)
admin.site.register(models.Lesson , lessonAdmin)
admin.site.register(models.Topic , topicAdmin)
admin.site.register(models.Chapter , chapterAdmin)
admin.site.register(models.Exponential_answer)
admin.site.register(models.Answers)
admin.site.register(models.Quizzes_status)

