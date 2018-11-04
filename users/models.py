# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals  import post_save
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import ContentType , GenericForeignKey
from core.models.temporaryKey import BaseTemporaryKey
from core.models.lessonTree import LESSON , GRADE , allowed_types , LessonTree
    



class Email_auth(BaseTemporaryKey):
    user = models.OneToOneField(User)
    FOEWARD_TIME = 1800 #00:30:00 
    def cleaner_action(self):
        self.user.delete()
        self.delete()
        
    def __unicode__(self):
        return u'username: {0} ;;; add date: {1} ;;; remove date: {2}'.format(
            self.user.username,self.add_date, self.remove_date)
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
    grade = models.ForeignKey(LessonTree,null = True , blank = True , related_name='grade')
    interest_lesson = models.ForeignKey(LessonTree , blank = True , related_name='interest_lesson')
    score = models.IntegerField(blank = True)
    
    @allowed_types(GRADE , grade)
    @allowed_types(LESSON , interest_lesson)
    def save(self ,**kwargs):
        return super(Profile,self).save(**kwargs)


    class Meta:
        db_table = "profile"
    def __unicode__(self):
        return u'{0}'.format(self.user.username)


class FeedBack(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    FEEDBACK_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User)
    feedback_type = models.CharField(max_length=1, choices=FEEDBACK_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()