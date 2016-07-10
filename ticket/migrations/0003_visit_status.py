# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-10 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20160708_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='status',
            field=models.CharField(choices=[('W', 'Waiting'), ('D', 'Done')], default='W', max_length=10),
        ),
    ]
