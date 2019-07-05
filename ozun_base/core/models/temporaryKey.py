# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class BaseTemporaryKey(models.Model):
    """ base class for all model classes that want be temporary , mean 
        after a determined time something happen for them
        NOTE: use 'create_record' for create a object insted 'save' """

    add_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField()
    FORWARD_TIME = 600 # by second # 00:10:00

    def create_record(self ,forward_time = 0,*args,**kwargs):
        if forward_time == 0:
            forward_time =self.FORWARD_TIME
        time = timezone.now()
        self.close_date = time + timezone.timedelta(0,forward_time)
        
        return self
    def close_action(self):
        """ how behaive with object if he get out of date """
        self.delete()


    class Meta:
        abstract = True
