# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('encrypted', models.BooleanField(default=False)),
                ('path', models.FileField(default=None, upload_to='attachments', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Nathan\\Documents\\UVA\\Semester 4\\CS 3240\\final project\\cs3240-f16-team07\\dev\\safecollab\\media'), null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='creator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
