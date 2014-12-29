# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0007_auto_20141215_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='pack_type',
            field=models.CharField(max_length=200, choices=[('ACTUALITE', 'Actualite'), ('REPORTAGE', 'Reportage')], default='ACTUALITE', verbose_name='type'),
            preserve_default=True,
        ),
    ]
