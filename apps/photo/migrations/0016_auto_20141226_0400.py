# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0015_auto_20141215_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', to='photo.Pack', null=True, editable=False)),
            ],
            options={
                'db_table': 'photo_pack_translation',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='packtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='pack',
            name='description',
        ),
        migrations.RemoveField(
            model_name='pack',
            name='label',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='description',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='label',
        ),
    ]
