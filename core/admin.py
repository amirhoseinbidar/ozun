# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory 

class MyAdmin(TreeAdmin):
    form = movenodeform_factory(models.LessonTree)

admin.site.register(models.LessonTree,MyAdmin)
admin.site.register(models.TreeContent)
admin.site.register(models.countries.Country_province)
admin.site.register(models.countries.Country_county)
admin.site.register(models.countries.Country_city)
admin.site.register(models.countries.Location)
admin.site.register(models.FeedBack)
