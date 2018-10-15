# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-15 06:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_auto_20181015_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administered_on', models.DateField(default=datetime.datetime.now)),
                ('administered_at', models.DateField(default=datetime.datetime.now)),
                ('baby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccine_records', to='operations.Baby')),
            ],
        ),
        migrations.RemoveField(
            model_name='phcvisit',
            name='baby',
        ),
        migrations.RemoveField(
            model_name='vaccinerecord',
            name='visit',
        ),
        migrations.AddField(
            model_name='vaccinerecord',
            name='status',
            field=models.CharField(choices=[(b'pending', b'Pending'), (b'scheduled', b'Scheduled'), (b'administered', b'Administered')], default='pending', max_length=20, verbose_name='Vaccine Status'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PHCVisit',
        ),
        migrations.AddField(
            model_name='vaccinerecord',
            name='phc',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='phc', to='operations.Appointment'),
            preserve_default=False,
        ),
    ]
