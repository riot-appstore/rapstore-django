# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-05 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180405_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='description',
            field=models.TextField(blank=True, max_length=65535, null=True),
        ),
    ]
