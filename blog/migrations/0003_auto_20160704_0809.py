# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 08:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160704_0705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='writer',
            new_name='user',
        ),
    ]
