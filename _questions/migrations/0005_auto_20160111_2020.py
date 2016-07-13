# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('_questions', '0004_answercomment_questioncomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('up', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VoteQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('up', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='votequestion',
            name='question',
            field=models.ForeignKey(to='_questions.Question'),
        ),
        migrations.AddField(
            model_name='votequestion',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='voteanswer',
            name='answer',
            field=models.ForeignKey(to='_questions.Answer'),
        ),
        migrations.AddField(
            model_name='voteanswer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
