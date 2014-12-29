# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0004_pack_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='pack_type',
            field=models.CharField(default='ACTUALITE', choices=[('ACTUALITE', 'Actualite'), ('REPORTAGE', 'Reportage')], max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pack',
            name='status',
            field=models.CharField(default='OFFLINE', choices=[('ONLINE', 'Online'), ('OFFLINE', 'Offline')], max_length=200),
            preserve_default=True,
        ),
    ]
