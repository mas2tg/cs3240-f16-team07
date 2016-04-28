# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20160424_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='path',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Nathan\\Documents\\UVA\\Semester 4\\CS 3240\\final project\\cs3240-f16-team07\\media'), null=True, default=None, upload_to='attachments'),
        ),
    ]
