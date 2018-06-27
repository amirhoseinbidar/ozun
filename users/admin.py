# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from users import models

# Register your models here.

admin.site.register(models.Email_auth)
admin.site.register(models.Profile)
