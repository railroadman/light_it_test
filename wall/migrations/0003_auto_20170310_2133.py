# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0002_auto_20170310_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
