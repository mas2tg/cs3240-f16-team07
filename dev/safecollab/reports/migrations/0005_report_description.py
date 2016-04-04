# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_report_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='description',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
