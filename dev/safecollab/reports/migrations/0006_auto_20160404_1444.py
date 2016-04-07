# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_report_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='path',
            field=models.FileField(upload_to=''),
        ),
    ]
