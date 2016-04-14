# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('encrypted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=50)),
                ('private', models.BooleanField(default=False)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
                ('path', models.FileField(default=None, upload_to='attachments', null=True, storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\Nathan\\Documents\\UVA\\Semester 4\\CS 3240\\final project\\cs3240-f16-team07\\dev\\safecollab\\media'))),
                ('creator', models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
