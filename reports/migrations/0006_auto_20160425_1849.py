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
            field=models.FileField(default=None, storage=django.core.files.storage.FileSystemStorage(location='/home/osboxes/safecollab/cs3240-f16-team07/media'), upload_to='attachments', null=True),
        ),
    ]
