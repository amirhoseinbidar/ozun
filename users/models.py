# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class email_auth(models.Model):
    user = models.OneToOneField(User)
    add_date = models.DateTimeField()
    remove_date = models.DateTimeField()
    

    def create_record(self ,person = User):
        time = timezone.now()
        remove_time = time + timezone.timedelta(minutes = 30)

        user = email_auth.objects.create(user = person,
            add_date = time, remove_date = remove_time)
        user.save()

    def delete(self, *args, **kwargs): 
        self.user.delete()  
        return super(self.__class__, self).delete(*args, **kwargs)
       
    def __unicode__(self):
        return u'username:{0} ;;; add date:{1} ;;; remove date:{2}'.format(self.user.username,self.add_date, self.remove_date)



