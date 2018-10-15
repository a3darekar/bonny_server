# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-15 06:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_auto_20181006_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='PHCVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administered_on', models.DateField(default=datetime.datetime.now)),
                ('administered_at', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(choices=[(b'pending', b'Pending'), (b'scheduled', b'Scheduled'), (b'administered', b'Administered')], max_length=20, verbose_name='Vaccine Status')),
            ],
        ),
        migrations.RemoveField(
            model_name='vaccinerecord',
            name='administered_at',
        ),
        migrations.RemoveField(
            model_name='vaccinerecord',
            name='administered_on',
        ),
        migrations.RemoveField(
            model_name='vaccinerecord',
            name='baby',
        ),
        migrations.RemoveField(
            model_name='vaccinerecord',
            name='status',
        ),
        migrations.AddField(
            model_name='baby',
            name='week',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vaccinerecord',
            name='amount',
            field=models.PositiveIntegerField(default=10, help_text='Dosage amount in ml', verbose_name='Dosage Amount'),
        ),
        migrations.AddField(
            model_name='vaccinerecord',
            name='dose',
            field=models.CharField(default='Generic Doesage', help_text='name of vaccine dose with Company name', max_length=90),
        ),
        migrations.AddField(
            model_name='phcvisit',
            name='baby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccine_records', to='operations.Baby'),
        ),
        migrations.AddField(
            model_name='vaccinerecord',
            name='visit',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='visit', to='operations.PHCVisit'),
            preserve_default=False,
        ),
    ]
