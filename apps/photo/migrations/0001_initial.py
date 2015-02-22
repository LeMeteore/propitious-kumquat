# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taxonomy', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date published', models.DateField(default=datetime.datetime.now)),
                ('begin_date', models.DateField(verbose_name='begin_date', default=datetime.datetime.now)),
                ('end_date', models.DateField(verbose_name='end_date', default=datetime.datetime.now)),
                ('countries', models.ManyToManyField(to='taxonomy.Country')),
                ('domain', models.ForeignKey(verbose_name='domain', to='taxonomy.Domain')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200)),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(to='photo.Pack', editable=False, null=True, related_name='translations')),
            ],
            options={
                'abstract': False,
                'db_table': 'photo_pack_translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('description', models.TextField(verbose_name='description', max_length=200)),
                ('license', models.CharField(verbose_name='license', max_length=200)),
                ('width', models.IntegerField(verbose_name='width', max_length=200)),
                ('height', models.IntegerField(verbose_name='heigth', max_length=200)),
                ('camera_model', models.CharField(verbose_name='camera_model', max_length=200)),
                ('sensibilite_iso', models.CharField(verbose_name='sensibilite_iso', max_length=200)),
                ('focal', models.CharField(verbose_name='focal', max_length=200)),
                ('ouverture', models.CharField(verbose_name='ouverture', max_length=200)),
                ('temps_de_pause', models.CharField(verbose_name='temps_de_pause', max_length=200)),
                ('image', models.ImageField(upload_to='wappa', max_length=200)),
                ('date published', models.DateField(default=datetime.datetime.now)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('countries', models.ManyToManyField(to='taxonomy.Country', verbose_name='countries')),
                ('photo_tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', blank=True, help_text='A comma-separated list of tags.')),
                ('status', models.ForeignKey(verbose_name='status', to='taxonomy.Status')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='packtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='pack',
            name='image',
            field=models.ForeignKey(to='photo.Photo', null=True, verbose_name='image preview', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pack',
            name='pack_tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', blank=True, help_text='A comma-separated list of tags.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pack',
            name='pack_type',
            field=models.ForeignKey(verbose_name='type', to='taxonomy.Gender'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pack',
            name='photos',
            field=models.ManyToManyField(to='photo.Photo', null=True, blank=True, related_name='packs'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pack',
            name='status',
            field=models.ForeignKey(verbose_name='status', to='taxonomy.Status'),
            preserve_default=True,
        ),
    ]
