# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 21:33
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_server', '0005_auto_20170716_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='content',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]