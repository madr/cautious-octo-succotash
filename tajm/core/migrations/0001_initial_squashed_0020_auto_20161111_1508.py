# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-10-15 05:31
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tajm.core.models


class Migration(migrations.Migration):

    replaces = [('core', '0001_initial'), ('core', '0002_auto_20160314_2101'), ('core', '0003_auto_20160511_0624'), ('core', '0004_auto_20160515_1102'), ('core', '0005_auto_20160515_1105'), ('core', '0006_auto_20160515_1106'), ('core', '0007_auto_20160515_1112'), ('core', '0008_auto_20160515_1116'), ('core', '0009_auto_20160515_1118'), ('core', '0010_auto_20160515_1119'), ('core', '0011_auto_20160515_1122'), ('core', '0012_auto_20160515_1127'), ('core', '0013_auto_20160518_0712'), ('core', '0014_auto_20161106_1011'), ('core', '0015_auto_20161106_1016'), ('core', '0016_auto_20161111_1222'), ('core', '0017_auto_20161111_1349'), ('core', '0018_auto_20161111_1351'), ('core', '0019_auto_20161111_1352'), ('core', '0020_auto_20161111_1508')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(default=15)),
                ('note', models.TextField()),
                ('done_at', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'progresses',
                'ordering': ['-done_at'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('billable', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'projects',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='progress',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='progress',
            name='duration',
            field=models.IntegerField(default=15, validators=[django.core.validators.MinValueValidator(15), tajm.core.models.validate_duration]),
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(default=480, validators=[django.core.validators.MinValueValidator(15), tajm.core.models.validate_duration])),
                ('note', models.TextField(blank=True, default='')),
                ('done_at', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.AbsenceCategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TajmUser')),
                ('started_at', models.TimeField(default='00:00:00')),
            ],
            options={
                'ordering': ['-done_at'],
                'verbose_name_plural': 'absences',
            },
        ),
        migrations.CreateModel(
            name='AbsenceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'reasons',
            },
        ),
        migrations.AlterModelOptions(
            name='absencecategory',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='progress',
            options={'ordering': ['-done_at', 'created_at'], 'verbose_name_plural': 'progresses'},
        ),
        migrations.AddField(
            model_name='progress',
            name='started_at',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.CreateModel(
            name='TajmUser',
            fields=[
            ],
            options={
                'db_table': 'auth_user',
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='progress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.TajmUser'),
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128)),
                ('ends_at', models.DateField(blank=True, null=True)),
                ('starts_at', models.DateField(blank=True, null=True)),
                ('hour_amount', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
            ],
        ),
        migrations.AlterField(
            model_name='progress',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AlterModelOptions(
            name='deadline',
            options={'ordering': ['-ends_at', '-starts_at'], 'verbose_name_plural': 'deadlines'},
        ),
        migrations.RemoveField(
            model_name='deadline',
            name='project',
        ),
        migrations.AddField(
            model_name='deadline',
            name='projects',
            field=models.ManyToManyField(to='core.Project'),
        ),
    ]
