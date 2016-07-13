# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_questions', '0007_auto_20160125_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerrevision',
            name='sophistication',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionrevision',
            name='sophistication',
            field=models.IntegerField(default=0),
        ),
    ]
