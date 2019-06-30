# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey
from django.contrib.auth.models import User


class FeedBack(models.Model):
    FAVORITE = 'F'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    FEEDBACK_TYPES = (
        (FAVORITE, 'favorite'),
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


UP_VOTE = FeedBack.UP_VOTE
DOWN_VOTE = FeedBack.DOWN_VOTE
FAVORITE = FeedBack.FAVORITE