# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 09:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mail_server', '0004_auto_20170716_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='mail_server.Template'),
        ),
    ]
