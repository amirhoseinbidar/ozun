# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import course , magazine

# Register your models here.

admin.site.register(course)
admin.site.register(magazine)