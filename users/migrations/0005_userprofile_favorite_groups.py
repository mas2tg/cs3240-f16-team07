# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('users', '0004_auto_20160424_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favorite_groups',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
    ]
