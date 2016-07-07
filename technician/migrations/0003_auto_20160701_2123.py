# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-01 21:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('technician', '0002_technician_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='middle_name',
            field=models.CharField(default=datetime.datetime(2016, 7, 1, 21, 23, 22, 501044, tzinfo=utc), max_length=120),
            preserve_default=False,
        ),
    ]
