# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 12:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dongzip', '0016_profile_favorite_society'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorite_society',
        ),
    ]
