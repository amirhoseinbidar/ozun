# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import LessonTree ,TreeContent
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory 

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(LessonTree)

admin.site.register(LessonTree,MyAdmin)
admin.site.register(TreeContent)