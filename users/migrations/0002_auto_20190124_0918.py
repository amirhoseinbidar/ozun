# Generated by Django 2.1.3 on 2019-01-24 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email_auth',
            name='user',
        ),
        migrations.DeleteModel(
            name='Email_auth',
        ),
    ]
