# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-18 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20170112_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='photodb',
            name='originLink',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
