# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals  import post_save
from quizzes.models import Grade , Lesson
from django.core.exceptions import ValidationError
from quizzes.models import Quizzes ,Quizzes_status


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
    class Meta:
        abstract = True

class BaseQuizzesInfo(models.Model):
    user = models.ForeignKey(User)
    quizzes_status = models.ManyToManyField(Quizzes_status,blank = True)

    class Meta:
        abstract = True
    def __unicode__(self):
        return u"{0}".format(self.user)
    

class QuizzesInfo(BaseTemporaryKey , BaseQuizzesInfo):
    key = models.CharField(max_length = 100 , blank = True)
    is_active = models.BooleanField() 
    
    def create_record(self,user,quizzes_status,key, forward_time = 0,is_active = True,*args,**kwargs ): 
        if self.__class__.objects.filter(key = key).exists():# should not a key duplicate
            raise ValidationError('this key is alredy exist')
        
        super(self.__class__,self).create_record(forward_time,*args,**kwargs)
        self.key = key
        self.is_active = is_active
        self.user = user
        self.save()
        self.quizzes_status = quizzes_status
        self.save()
        return self

    def isOutOfDate(self):
        print timezone.now() 
        print self.close_date
        if timezone.now() >= self.close_date:
            return True   
        return False 
    def disable(self):
        self.is_active = False
        self.key = ''
        self.save()
    
    def __unicode__(self):
        if timezone.now() > self.close_date :
            return u'key {0} is out of date'.format(self.key)
        return u'key: {0} ;;; {1} later will delete'.format(self.key,self.close_date - timezone.now() )

    



class Email_auth(BaseTemporaryKey):
    user = models.OneToOneField(User)
    FOEWARD_TIME = 1800 #00:30:00 
  
    def __unicode__(self):
        return u'username: {0} ;;; add date: {1} ;;; remove date: {2}'.format(self.user.username,self.add_date, self.remove_date)
    class Meta:
        db_table = "email_auth"
 
@receiver(post_save,sender = User)
def create_models(sender,instance,created, **kwargs):
    if created:
        Email_auth().create_record(user = instance)


class Country_province(models.Model):
    name = models.CharField(max_length = 50)
    class Meta:
        db_table = "province"
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Country_county(models.Model):
    province = models.ForeignKey(Country_province)
    name = models.CharField(max_length = 50)
    class Meta:
        db_table = "county"
    def __unicode__(self):
        return u'{0}/{1}'.format(self.province.name,self.name)

class Country_city(models.Model):
    county = models.ForeignKey(Country_county)
    name = models.CharField(max_length = 50)
    class Meta:
        db_table = "city"
        
    def __unicode__(self):
        return u'{0}/{1}/{2}'.format(self.county.province.name,self.county.name,self.name)

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.ForeignKey(Country_city, null= True ,blank= True  )
    bio = models.TextField(blank=True)
    image = models.ImageField(blank = True,upload_to='users/images')
    brith_day = models.DateField(null = True , blank = True)
    grade = models.ForeignKey(Grade,null = True , blank = True )
    interest_lesson = models.ManyToManyField(Lesson , blank = True)
    score = models.IntegerField(blank = True)
    
    class Meta:
        db_table = "profile"
    def __unicode__(self):
        return u'{0}'.format(self.user.username)




    
