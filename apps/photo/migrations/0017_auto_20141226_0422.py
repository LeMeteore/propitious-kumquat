# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0016_auto_20141226_0400'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(related_name='translations', to='photo.Photo', editable=False, null=True)),
            ],
            options={
                'abstract': False,
                'db_table': 'photo_photo_translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='phototranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
