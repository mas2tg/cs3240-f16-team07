# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0002_auto_20160409_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='encrypted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='key',
            field=models.BinaryField(default=None, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
