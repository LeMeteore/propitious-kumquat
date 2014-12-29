# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0014_photo_pack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
