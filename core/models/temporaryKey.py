# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class BaseTemporaryKey(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    FORWARD_TIME = 600 # by second # 00:10:00

    def create_record(self ,forward_time = 0,*args,**kwargs):
        if forward_time == 0:
            forward_time =self.FORWARD_TIME
        time = timezone.now()
        self.close_date = time + timezone.timedelta(0,forward_time)
        
        return self
    def cleaner_action(self):
        self.delete()

    class Meta:
        abstract = True
