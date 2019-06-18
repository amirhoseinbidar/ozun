# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey
from core.models.temporaryKey import BaseTemporaryKey
from core.models import LESSON, GRADE, allowed_types, LessonTree, Location
from django.urls import reverse
from datetime import datetime
from allauth.socialaccount import default_app_config
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.account.models import EmailAddress
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from quizzes.models import ExamStatistic


@receiver(user_signed_up)
def createProfile(request, user, **kwargs):
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(
            user=user,
            image='users/diffalte_images/(1).jpg'
        )


@receiver(post_save, sender=ExamStatistic)
def score_update(instance, **kwargs):
    Profile.objects.get(user=instance.exam.user).count_score()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.SET_NULL)
    bio = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='users/images')
    brith_day = models.DateField(null=True, blank=True)
    grade = models.ForeignKey(
        LessonTree, null=True, blank=True, related_name='grade', on_delete=models.SET_NULL)
    interest_lesson = models.ForeignKey(LessonTree, blank=True,
                                        null=True, related_name='interest_lesson', on_delete=models.SET_NULL)
    score = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        allowed_types(GRADE, self.grade, 'grade')
        allowed_types(LESSON, self.interest_lesson, 'interest_lesson')
        if not self.score:
            self.score = 0

        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})

    def get_user_age(self):
        if self.brith_day:
            try:
                brith_day = datetime(
                    year=self.brith_day.year,
                    month=self.brith_day.month,
                    day=self.brith_day.day,
                )
            except AttributeError:
                brith_day = None

            deffrence = datetime.today() - brith_day
            age_year = deffrence.days // (365.25)
            age_month = (deffrence.days - age_year * 365.25)//(365.25/12)

        else:
            age_year = age_month = 0

        return (age_year, age_month)

    def count_score(self):
        self.score = ExamStatistic.objects.filter(
            exam__user=self.user).aggregate(Sum('total_score'))['total_score__sum']
        self.save()

    class Meta:
        db_table = "profile"

    def __unicode__(self):
        return u'{0}'.format(self.user.username)
