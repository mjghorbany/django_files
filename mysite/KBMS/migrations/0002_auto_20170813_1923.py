# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-13 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KBMS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rel_type', models.CharField(max_length=10)),
                ('rel_title', models.CharField(max_length=250)),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='node',
            old_name='node',
            new_name='ini_node',
        ),
        migrations.AddField(
            model_name='rel',
            name='rel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KBMS.Node'),
        ),
    ]
