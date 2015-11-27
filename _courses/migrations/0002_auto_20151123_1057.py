# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='component',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='course',
            name='name',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='name',
        ),
        migrations.AddField(
            model_name='component',
            name='slide',
            field=models.ForeignKey(to='_courses.Slide', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='component',
            name='title',
            field=models.CharField(max_length=254, default='title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=254, default='title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='title',
            field=models.CharField(max_length=254, default='title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slide',
            name='title',
            field=models.CharField(max_length=254, default='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='component',
            name='type',
            field=models.IntegerField(choices=[(1, 'Text'), (2, 'Image')]),
        ),
    ]
