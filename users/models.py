# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import ContentType , GenericForeignKey
from core.models.temporaryKey import BaseTemporaryKey
from core.models import LESSON , GRADE , allowed_types , LessonTree ,Location 



class Email_auth(BaseTemporaryKey):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    FORWARD_TIME = 1800 #00:30:00 

    def create_record(self,user,forward_time = 0,*args,**kwargs):
        self = super(Email_auth,self).create_record(forward_time)
        self.user = user
        return self.save(*args,**kwargs)


    def cleaner_action(self):
        self.user.delete()
        self.delete()
        
    def __str__(self):
        return self.user.__str__()
    class Meta:
        db_table = "email_auth"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null= True 
        ,blank= True, on_delete=models.SET_NULL )
    bio = models.TextField(blank=True)
    image = models.ImageField(blank = True,upload_to='users/images')
    brith_day = models.DateField(null = True , blank = True)
    grade = models.ForeignKey(LessonTree,null = True , blank = True 
        , related_name='grade', on_delete=models.SET_NULL)
    interest_lesson = models.ForeignKey(LessonTree , blank = True ,
        null = True , related_name='interest_lesson',on_delete=models.SET_NULL)
    score = models.IntegerField(blank = True , null=True)

    
    def save(self ,*args,**kwargs):
        allowed_types(GRADE , self.grade,'grade')
        allowed_types(LESSON , self.interest_lesson , 'interest_lesson')
        if not self.score:
            self.score = 0

        return super(Profile,self).save(*args,**kwargs)


    class Meta:
        db_table = "profile"
    def __unicode__(self):
        return u'{0}'.format(self.user.username)


class FeedBack(models.Model):
    FAVORITE = 'F'
    #LIKE = 'L'  I dont know why like should be but maybe will use it
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    FEEDBACK_TYPES = (
        (FAVORITE, 'favorite'),
    #    (LIKE, 'Like'),
        (UP_VOTE, 'up vote'),
        (DOWN_VOTE, 'down vote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=1, choices=FEEDBACK_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()