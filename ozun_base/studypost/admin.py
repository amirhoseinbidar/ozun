# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models 

class CourseSubPostInline(admin.StackedInline):
    model = models.CourseSubPost
    raw_id_fields = ('lesson' ,)

class CourseAdmin(admin.ModelAdmin):
    inlines = (CourseSubPostInline , )
    raw_id_fields = ('lesson' ,)
    text_fields_search = ('content' , 'title' , 'sub_posts__content')
    readonly_fields = ('slug','total_votes')

admin.site.register(models.Course , CourseAdmin)
admin.site.register(models.Magazine)