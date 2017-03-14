# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 15:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('oauth_id', models.IntegerField(blank=True, null=True)),
                ('service', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('photo', models.URLField(blank=True, default=0, null=True)),
                ('total_comments', models.IntegerField(blank=True, default=0, null=True)),
                ('logged_at', models.DateField(blank=True, null=True)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'authors',
            },
        ),
    ]
