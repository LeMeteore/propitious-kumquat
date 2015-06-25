# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_auto_20150222_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pack',
            name='date published',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='date published',
        ),
        migrations.AddField(
            model_name='pack',
            name='pub_date',
            field=models.DateField(verbose_name='date published', default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='exif_date',
            field=models.DateField(verbose_name='date exif', default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='pub_date',
            field=models.DateField(verbose_name='date published', default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
