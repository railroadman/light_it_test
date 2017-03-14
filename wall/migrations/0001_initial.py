# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 15:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('soc_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('msg_type', models.IntegerField(blank=True, null=True)),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('root_parent_id', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soc_auth.Authors')),
            ],
            options={
                'db_table': 'messages',
            },
        ),
    ]