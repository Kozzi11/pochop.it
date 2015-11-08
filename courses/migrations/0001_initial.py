# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompoenentConfig',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key', models.IntegerField()),
                ('value', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Text'), (1, 'Image')])),
                ('order', models.IntegerField()),
                ('parent', models.ForeignKey(to='courses.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('order', models.IntegerField()),
                ('courses', models.ForeignKey(to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('lesson', models.ForeignKey(to='courses.Lesson')),
            ],
        ),
        migrations.AddField(
            model_name='compoenentconfig',
            name='component',
            field=models.ForeignKey(to='courses.Component'),
        ),
    ]
