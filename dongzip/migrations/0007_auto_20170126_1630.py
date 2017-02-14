# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dongzip', '0006_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(null=True, upload_to='uploaded/user_profile/'),
        ),
        migrations.AlterField(
            model_name='school',
            name='logo_image',
            field=models.ImageField(null=True, upload_to='uploaded/school_profile/'),
        ),
        migrations.AlterField(
            model_name='society',
            name='background_image',
            field=models.ImageField(null=True, upload_to='uploaded/society_profile/'),
        ),
        migrations.AlterField(
            model_name='society',
            name='logo_image',
            field=models.ImageField(null=True, upload_to='uploaded/society_profile/'),
        ),
    ]
