# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 07:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dongzip', '0011_auto_20170210_1626'),
    ]

    operations = [
        migrations.RenameField(
            model_name='society',
            old_name='society',
            new_name='categorys',
        ),
    ]