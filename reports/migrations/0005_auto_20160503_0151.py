# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0004_report_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('path', models.FileField(default=None, storage=django.core.files.storage.FileSystemStorage(location='/home/osboxes/safecollab/cs3240-f16-team07/media'), null=True, upload_to='attachments')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='folder_creator')),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='path',
        ),
        migrations.AddField(
            model_name='report',
            name='city',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='report',
            name='country',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='report',
            name='keyword',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='report',
            name='region',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='report',
            name='region_code',
            field=models.CharField(blank=True, null=True, max_length=30),
        ),
        migrations.AddField(
            model_name='file',
            name='report',
            field=models.ForeignKey(blank=True, to='reports.Report', related_name='files', null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(blank=True, to='reports.Folder', related_name='folder', null=True),
        ),
    ]
