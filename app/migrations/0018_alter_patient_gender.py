# Generated by Django 4.2.11 on 2024-03-30 01:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0017_rename_hdl_cholestrol_patient_hdl_cholesterol_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("Male", "Male"), ("Female", "Female")],
                max_length=6,
                null=True,
            ),
        ),
    ]
