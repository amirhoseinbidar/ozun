# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quizzes import models
# Register your models here.
admin.site.register(models.grade)
admin.site.register(models.lesson)
admin.site.register(models.level)
admin.site.register(models.quizze)
admin.site.register(models.source)