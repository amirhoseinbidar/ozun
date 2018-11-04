# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-04 12:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LessonTree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TreeContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('G', 'grade'), ('L', 'lesson'), ('C', 'chapter'), ('T', 'topic')], max_length=1)),
            ],
        ),
        migrations.AddField(
            model_name='lessontree',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TreeContent'),
        ),
    ]
