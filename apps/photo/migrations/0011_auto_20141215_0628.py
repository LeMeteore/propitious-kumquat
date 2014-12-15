# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0010_pack_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='country',
            field=models.ManyToManyField(to='photo.Country'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='status',
            field=models.CharField(default='OFFLINE', max_length=200, choices=[('ONLINE', 'Online'), ('OFFLINE', 'Offline')]),
            preserve_default=True,
        ),
    ]
