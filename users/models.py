# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals  import post_save
from quizzes.models import Grade , Lesson

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
		
		

 
@receiver(post_save,sender = User)
def create_models(sender,instance,created, **kwargs):
    if created:
        Email_auth().save_record(user = instance)





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
    province = models.ForeignKey(Country_province)
    county = models.ForeignKey(Country_county)
    name = models.CharField(max_length = 50)
    class Meta:
        db_table = "city"
    def __unicode__(self):
        return u'{0}/{1}/{2}'.format(self.province.name,self.county.name,self.name)

class Profile(models.Model):
    user = models.OneToOneField(User)
    location = models.ForeignKey(Country_city, null= True ,blank= True  )
    bio = models.TextField(blank=True)
    image = models.ImageField(blank = True,upload_to='users/images')
    brith_day = models.DateField(null = True , blank = True)
    grade = models.ForeignKey(Grade,null = True , blank = True )
    interest_lesson = models.ForeignKey(Lesson,null = True , blank = True)
    models.Manager
    class Meta:
        db_table = "profile"
    def __unicode__(self):
        return u'{0}'.format(self.user.username)


from quizzes.models import Quizze 

class UsersInfo(models.Model):
    user = models.ForeignKey(User)
    quizzes = models.ManyToManyField(Quizze)
    status = models.TextField() # information store here by Json format
    date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        db_table = "users_info"
    def __unicode__(self):
        return u"{0} , {1}".format(self.user,self.date)

    
