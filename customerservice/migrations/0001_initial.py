# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-26 21:31
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('mobile_number', models.CharField(blank=True, max_length=11, unique=True, validators=[django.core.validators.RegexValidator('\\d{11}', 'Please enter a valid mobile number.')])),
                ('land_phone_number', models.CharField(max_length=8, unique=True, validators=[django.core.validators.RegexValidator('\\d{8}', 'Please enter a valid phone number.')])),
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('block_number', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('serial_number', models.BigIntegerField(unique=True)),
                ('purchase_date', models.DateField()),
                ('last_maintenance_date', models.DateField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customerservice.Customer')),
            ],
        ),
    ]