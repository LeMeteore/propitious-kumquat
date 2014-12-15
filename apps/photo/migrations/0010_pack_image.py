# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0009_pack_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='image',
            field=models.ImageField(upload_to='wappa', max_length=200, default='wappa/Capture_décran_-_23112014_-_224647.png'),
            preserve_default=False,
        ),
    ]
