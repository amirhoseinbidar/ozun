# Generated by Django 2.1.1 on 2019-06-19 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190213_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
    ]
