# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inbox', '0005_message_blue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='blue',
        ),
    ]
