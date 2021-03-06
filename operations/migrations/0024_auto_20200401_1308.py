# Generated by Django 3.0.4 on 2020-04-01 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import operations.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0023_auto_20200401_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinitian',
            name='user',
            field=models.ForeignKey(help_text='Create a new user to add as a  Clinitian. This would be used as login credentials.', on_delete=models.SET(operations.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='parent',
            name='user',
            field=models.ForeignKey(help_text='Create a new user to add as a Parent or Guardian. This would be used as login credentials.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
