# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_courses', '0002_auto_20151121_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='slide',
            field=models.ForeignKey(to='_courses.Slide', default=0),
            preserve_default=False,
        ),
    ]
