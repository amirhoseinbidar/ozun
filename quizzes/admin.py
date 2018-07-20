# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models
# Register your models here.
admin.site.register(models.Level)
admin.site.register(models.Quizze)
admin.site.register(models.Source)
admin.site.register(models.Grade)
admin.site.register(models.Lesson)
admin.site.register(models.Topic)
admin.site.register(models.Chapter)
admin.site.register(models.Exponential_answer)
