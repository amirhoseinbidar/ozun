# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals  import post_save

# Create your models here.
class Email_auth(models.Model):
    user = models.OneToOneField(User)
    add_date = models.DateTimeField()
    remove_date = models.DateTimeField()
    

    def save_record(self ,user):
        time = timezone.now()
        remove_time = time + timezone.timedelta(minutes = 30)
       
        auth = Email_auth.objects.create(user = user,
            add_date = time, remove_date = remove_time)
        auth.save()

    def delete(self, *args, **kwargs): 
        self.user.delete()  
        return super(self.__class__, self).delete(*args, **kwargs)
       
    def __unicode__(self):
        return u'username:{0} ;;; add date:{1} ;;; remove date:{2}'.format(self.user.username,self.add_date, self.remove_date)
    class Meta:
        db_table = "email_auth"


class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(blank = True,upload_to='images/')
    brith_day = models.DateField(null = True , blank = True)

    class Meta:
        db_table = "profile"
    def __unicode__(self):
        return u'{0}'.format(self.user.username)
 
@receiver(post_save,sender = User)
def create_models(sender,instance,created, **kwargs):
    if created:
        Email_auth().save_record(user = instance)
       


