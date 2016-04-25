# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('body', models.CharField(max_length=2000)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2016, 4, 9, 15, 10, 17, 803916))),
                ('read', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='recipient')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sender')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
