# Generated by Django 3.0.4 on 2020-03-31 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operations', '0020_auto_20190812_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='administered_at',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phc', to='operations.HealthCare'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('scheduled', 'Scheduled'), ('partial', 'Partially Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=50),
        ),
        migrations.AlterField(
            model_name='baby',
            name='blood_group',
            field=models.CharField(choices=[('a_positive', 'A Positive'), ('a_negative', 'A Negative'), ('b_positive', 'B Positive'), ('b_negative', 'B Negative'), ('o_positive', 'O Positive'), ('o_negative', 'O Negative'), ('ab_positive', 'AB Positive'), ('ab_negative', 'AB Negative')], max_length=12, verbose_name='Blood Group'),
        ),
        migrations.AlterField(
            model_name='baby',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='baby',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='baby', to='operations.Parent'),
        ),
        migrations.AlterField(
            model_name='clinitian',
            name='HealthCare',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.HealthCare'),
        ),
        migrations.AlterField(
            model_name='clinitian',
            name='user',
            field=models.OneToOneField(help_text='Create a new user to add as a  Clinitian. This would be used as login credentials.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notif_type',
            field=models.CharField(choices=[('info', 'info'), ('success', 'success'), ('error', 'error'), ('danger', 'danger')], default='info', max_length=40, verbose_name='Notification Type'),
        ),
        migrations.AlterField(
            model_name='parent',
            name='user',
            field=models.OneToOneField(help_text='Create a new user to add as a Parent or Guardian. This would be used as login credentials.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vaccinerecord',
            name='status',
            field=models.CharField(choices=[('cancelled', 'Cancelled'), ('scheduled', 'Scheduled'), ('administered', 'Administered')], default='scheduled', max_length=20, verbose_name='Vaccine Status'),
        ),
        migrations.AlterField(
            model_name='vaccinerecord',
            name='vaccine',
            field=models.CharField(choices=[(0, (('bcg', 'BCG'), ('opv', 'OPV0'), ('hepb1', 'HEP-B 1'))), (6, (('dt1', 'DTwP 1'), ('ipv1', 'IPV 1'), ('hepb2', 'HEP-B 2'), ('hib1', 'HIB 1'), ('rota1', 'Rotavirus 1'), ('pcv1', 'PCV 1'))), (10, (('dt2', 'DTwP 2'), ('ipv2', 'IPV 2'), ('hib2', 'HIB 2'), ('rota2', 'Rotavirus 2'), ('pcv2', 'PCV 2'))), (14, (('dt3', 'DTwP 3'), ('ipv3', 'IPV 3'), ('hib3', 'HIB 3'), ('rota3', 'Rotavirus 3'), ('pcv3', 'PCV 3'))), (24, (('opv1', 'OPV 1'), ('hepb3', 'HEP-B 3'))), (36, (('opv2', 'OPV 2'), ('mmr1', 'MMR-1')))], max_length=20, verbose_name='Vaccine'),
        ),
        migrations.AlterField(
            model_name='vaccineschedule',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('scheduled', 'Scheduled'), ('administered', 'Administered')], max_length=20, verbose_name='Vaccine Status'),
        ),
        migrations.AlterField(
            model_name='vaccineschedule',
            name='vaccine',
            field=models.CharField(choices=[(0, (('bcg', 'BCG'), ('opv', 'OPV0'), ('hepb1', 'HEP-B 1'))), (6, (('dt1', 'DTwP 1'), ('ipv1', 'IPV 1'), ('hepb2', 'HEP-B 2'), ('hib1', 'HIB 1'), ('rota1', 'Rotavirus 1'), ('pcv1', 'PCV 1'))), (10, (('dt2', 'DTwP 2'), ('ipv2', 'IPV 2'), ('hib2', 'HIB 2'), ('rota2', 'Rotavirus 2'), ('pcv2', 'PCV 2'))), (14, (('dt3', 'DTwP 3'), ('ipv3', 'IPV 3'), ('hib3', 'HIB 3'), ('rota3', 'Rotavirus 3'), ('pcv3', 'PCV 3'))), (24, (('opv1', 'OPV 1'), ('hepb3', 'HEP-B 3'))), (36, (('opv2', 'OPV 2'), ('mmr1', 'MMR-1')))], max_length=20, verbose_name='Vaccine'),
        ),
    ]
