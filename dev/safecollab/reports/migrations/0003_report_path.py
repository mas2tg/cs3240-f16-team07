# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20160329_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='path',
            field=models.FileField(null=True, blank=True, upload_to=''),
        ),
    ]
