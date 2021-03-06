# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-05 15:19
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20180405_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_code', models.PositiveIntegerField(default=1)),
                ('version_name', models.CharField(max_length=255)),
                ('app_tarball', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/apps'), upload_to='')),
                ('is_public', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('has_dev_perm', 'Has dev permissions'),),
            },
        ),
        migrations.RemoveField(
            model_name='application',
            name='app_tarball',
        ),
        migrations.RemoveField(
            model_name='application',
            name='is_public',
        ),
        migrations.AddField(
            model_name='applicationinstance',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Application'),
        ),
        migrations.AlterUniqueTogether(
            name='applicationinstance',
            unique_together=set([('version_code', 'application')]),
        ),
    ]
