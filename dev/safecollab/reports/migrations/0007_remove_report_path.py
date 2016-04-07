# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20160404_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='path',
        ),
    ]
