# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-16 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20181114_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后台开发', max_length=20, verbose_name='课程类别'),
        ),
    ]
