# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-26 01:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('KBMS', '0003_auto_20170816_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ontology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=250)),
                ('ontology_title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=400)),
                ('album_logo', models.FileField(upload_to='')),
                ('is_available', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
