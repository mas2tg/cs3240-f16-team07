# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='user_id',
        ),
        migrations.AddField(
            model_name='report',
            name='creator',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='report_id',
            field=models.ForeignKey(to='reports.Report'),
        ),
    ]
