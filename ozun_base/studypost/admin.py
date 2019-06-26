# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Course , Magazine

# Register your models here.

admin.site.register(Course)
admin.site.register(Magazine)