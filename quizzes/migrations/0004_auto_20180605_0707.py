# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-05 07:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_auto_20180605_0704'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='grades',
            new_name='grade',
        ),
        migrations.RenameModel(
            old_name='lessons',
            new_name='lesson',
        ),
        migrations.RenameModel(
            old_name='levels',
            new_name='level',
        ),
        migrations.RenameModel(
            old_name='quizzes',
            new_name='quizze',
        ),
        migrations.RenameModel(
            old_name='sources',
            new_name='source',
        ),
        migrations.AlterModelTable(
            name='grade',
            table='grades',
        ),
        migrations.AlterModelTable(
            name='lesson',
            table='lessons',
        ),
        migrations.AlterModelTable(
            name='level',
            table='levels',
        ),
        migrations.AlterModelTable(
            name='quizze',
            table='quizzes',
        ),
        migrations.AlterModelTable(
            name='source',
            table='sources',
        ),
    ]