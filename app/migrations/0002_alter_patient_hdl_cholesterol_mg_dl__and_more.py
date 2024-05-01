# Generated by Django 4.2.11 on 2024-03-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='HDL Cholesterol (mg/dL)',
            field=models.PositiveIntegerField(choices=[(159, 'Less than 160'), (160, '160 - 199'), (200, '200 - 239'), (240, '240 - 279'), (280, '280+')]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Systolic Blood Pressure (mmHg)',
            field=models.PositiveIntegerField(choices=[(119, 'Less than 120'), (120, '120 - 129'), (130, '130 - 139'), (140, '140 - 159'), (160, '160 - 179'), (180, '180+')]),
        ),
        migrations.AlterField(
            model_name='patient',
            name='Total Cholesterol (mg/dL)',
            field=models.PositiveIntegerField(choices=[(159, 'Less than 160'), (160, '160 - 199'), (200, '200 - 239'), (240, '240 - 279'), (280, '280+')]),
        ),
    ]