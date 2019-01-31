# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from users import models
from django.utils.html import mark_safe
# Register your models here.
admin.site.site_header = 'ozun Admin'
admin.site.site_title = 'ozun Admin Portal'
admin.site.index_title = 'Welcome to ozun Admin Portal'

class profileAdmin(admin.ModelAdmin):
    readonly_fields = ["profile_image",]
    
    def profile_image(self, obj):
        
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=obj.image.width/4,
            height=obj.image.height/4,
            )
        )
class quizzesInfoAdmin(admin.ModelAdmin):
    list_display = ('id','is_active','close_date')
#admin.site.register(models.Email_auth)
admin.site.register(models.Profile,profileAdmin)
admin.site.register(models.FeedBack)
