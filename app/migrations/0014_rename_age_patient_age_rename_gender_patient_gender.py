# Generated by Django 4.2.11 on 2024-03-29 12:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0013_rename_age_patient_age_rename_gender_patient_gender"),
    ]

    operations = [
        migrations.RenameField(
            model_name="patient",
            old_name="AGE",
            new_name="Age",
        ),
        migrations.RenameField(
            model_name="patient",
            old_name="GENDER",
            new_name="Gender",
        ),
    ]
