# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 07:00
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
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('event_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('nickname', models.CharField(max_length=128)),
                ('tel_number', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=256)),
                ('member_number', models.IntegerField(default=0)),
                ('society_number', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Society',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('main_tel_number', models.CharField(max_length=32)),
                ('member_number', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True, max_length=512, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dongzip.School')),
                ('users', models.ManyToManyField(to='dongzip.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dongzip.School'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_event_set', to='dongzip.Society'),
        ),
        migrations.AddField(
            model_name='event',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_event_set', to='dongzip.Society'),
        ),
    ]
