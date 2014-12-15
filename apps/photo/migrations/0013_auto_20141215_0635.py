# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0012_remove_photo_pack'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='photo',
            name='date published',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
