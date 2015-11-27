# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompoenentConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('key', models.IntegerField()),
                ('value', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Text'), (1, 'Image')])),
                ('order', models.IntegerField()),
                ('parent', models.ForeignKey(to='_courses.models.ComponentData')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=300)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('order', models.IntegerField()),
                ('course', models.ForeignKey(to='_courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('lesson', models.ForeignKey(to='_courses.Lesson')),
            ],
        ),
        migrations.AddField(
            model_name='compoenentconfig',
            name='component',
            field=models.ForeignKey(to='_courses.models.ComponentData'),
        ),
    ]
