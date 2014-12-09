# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(max_length=200, upload_to='')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('pack', models.ForeignKey(to='photo.Pack')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
