# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='city',
            field=models.CharField(blank=True, null=True, max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='country',
            field=models.CharField(blank=True, null=True, max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='keyword',
            field=models.CharField(blank=True, null=True, max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='report',
            name='region_code',
            field=models.CharField(blank=True, null=True, max_length=30),
            preserve_default=True,
        ),
    ]
