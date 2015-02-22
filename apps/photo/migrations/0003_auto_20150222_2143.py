# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.photo.models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20150209_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(max_length=200, upload_to=apps.photo.models.Photo.content_file_name),
            preserve_default=True,
        ),
    ]
