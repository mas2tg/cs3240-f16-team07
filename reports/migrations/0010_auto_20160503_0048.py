# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_auto_20160502_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='path',
            field=models.FileField(null=True, upload_to='attachments', default=None, storage=django.core.files.storage.FileSystemStorage(location='/home/osboxes/safecollab/cs3240-f16-team07/media')),
        ),
    ]
