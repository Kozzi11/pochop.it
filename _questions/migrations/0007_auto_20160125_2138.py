# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('_questions', '0006_question_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerCommentScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('text', models.TextField()),
                ('editor_comment', models.TextField()),
                ('supervisor_comment', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnswerScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionCommentScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=254)),
                ('text', models.TextField()),
                ('editor_comment', models.TextField()),
                ('supervisor_comment', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionScrap',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='answer',
            name='scrap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='answercomment',
            name='scrap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='scrap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questioncomment',
            name='scrap',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='voteanswer',
            name='mits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='votequestion',
            name='mits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionscrap',
            name='question',
            field=models.ForeignKey(to='_questions.Question'),
        ),
        migrations.AddField(
            model_name='questionscrap',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questionrevision',
            name='question',
            field=models.ForeignKey(to='_questions.Question'),
        ),
        migrations.AddField(
            model_name='questionrevision',
            name='supervisor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=0, related_name='supervisor'),
        ),
        migrations.AddField(
            model_name='questionrevision',
            name='tags',
            field=models.ManyToManyField(to='_questions.Tag'),
        ),
        migrations.AddField(
            model_name='questioncommentscrap',
            name='question_comment',
            field=models.ForeignKey(to='_questions.QuestionComment'),
        ),
        migrations.AddField(
            model_name='questioncommentscrap',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answerscrap',
            name='answer',
            field=models.ForeignKey(to='_questions.Answer'),
        ),
        migrations.AddField(
            model_name='answerscrap',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answerrevision',
            name='answer',
            field=models.ForeignKey(to='_questions.Answer'),
        ),
        migrations.AddField(
            model_name='answerrevision',
            name='editor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answerrevision',
            name='supervisor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=0, related_name='answer_rev_supervisor'),
        ),
        migrations.AddField(
            model_name='answercommentscrap',
            name='answer_comment',
            field=models.ForeignKey(to='_questions.AnswerComment'),
        ),
        migrations.AddField(
            model_name='answercommentscrap',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
