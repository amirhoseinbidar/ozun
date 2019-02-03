# Generated by Django 2.1.3 on 2019-02-02 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country_city',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Country_county',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'county',
            },
        ),
        migrations.CreateModel(
            name='Country_province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'province',
            },
        ),
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
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=194)),
                ('city', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Country_city')),
            ],
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
        migrations.AddField(
            model_name='country_county',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Country_province'),
        ),
        migrations.AddField(
            model_name='country_city',
            name='county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Country_county'),
        ),
    ]
