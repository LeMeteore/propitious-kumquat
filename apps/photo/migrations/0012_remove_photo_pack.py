# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0011_auto_20141215_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='pack',
        ),
    ]
