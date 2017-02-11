# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-14 21:01
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models

import tajm.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='duration',
            field=models.IntegerField(default=15, validators=[django.core.validators.MinValueValidator(15), tajm.core.models.validate_duration]),
        ),
    ]