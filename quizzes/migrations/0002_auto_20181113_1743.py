# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-13 17:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessontree',
            name='content',
        ),
        migrations.DeleteModel(
            name='LessonTree',
        ),
        migrations.DeleteModel(
            name='TreeContent',
        ),
    ]
