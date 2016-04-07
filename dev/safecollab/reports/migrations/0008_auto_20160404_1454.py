# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_remove_report_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='report_id',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.AddField(
            model_name='report',
            name='path',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Nathan\\Documents\\UVA\\Semester 4\\CS 3240\\final project\\cs3240-f16-team07\\dev\\safecollab\\media'), default=None, upload_to='attachments'),
            preserve_default=True,
        ),
    ]
