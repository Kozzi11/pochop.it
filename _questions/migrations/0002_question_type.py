# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]
