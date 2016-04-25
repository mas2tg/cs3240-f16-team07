# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0004_report_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=30)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='folder_creator')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='report',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, related_name='folder', to='reports.Folder'),
            preserve_default=True,
        ),
    ]
