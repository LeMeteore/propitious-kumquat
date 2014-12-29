# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0005_auto_20141215_0532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pack',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='pack',
            name='date published',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
