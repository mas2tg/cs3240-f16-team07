# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20160426_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('path', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Nathan\\Documents\\UVA\\Semester 4\\CS 3240\\final project\\cs3240-f16-team07\\media'), null=True, default=None, upload_to='attachments')),
                ('report', models.ForeignKey(related_name='files', to='reports.Report', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='report',
            name='path',
        ),
    ]
