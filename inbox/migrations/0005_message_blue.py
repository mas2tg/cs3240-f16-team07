# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0004_auto_20160410_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='blue',
            field=models.BinaryField(null=True),
            preserve_default=True,
        ),
    ]
