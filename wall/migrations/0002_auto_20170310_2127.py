# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 19:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='created_at',
            field=models.DateField(auto_now_add=True, default='2017-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='messages',
            name='status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
