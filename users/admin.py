# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from users import models

# Register your models here.
admin.site.site_header = 'StudyLab Admin'
admin.site.site_title = 'StudyLab Admin Portal'
admin.site.index_title = 'Welcome to StudyLab Admin Portal'

admin.site.register(models.Email_auth)
admin.site.register(models.Profile)
admin.site.register(models.Country_province)
admin.site.register(models.Country_county)
admin.site.register(models.Country_city)
admin.site.register(models.QuizzesInfo)

