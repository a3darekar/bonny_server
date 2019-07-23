# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-23 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0015_auto_20190723_1357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='text_notifications',
        ),
        migrations.AddField(
            model_name='baby',
            name='text_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='baby',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Baby', to='operations.Baby'),
            preserve_default=False,
        ),
    ]
