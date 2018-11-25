# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-24 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=64)),
                ('port', models.CharField(max_length=8)),
                ('valid', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('other', models.CharField(max_length=256)),
            ],
        ),
    ]
