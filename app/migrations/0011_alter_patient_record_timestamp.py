# Generated by Django 4.2.11 on 2024-03-29 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_patient_record_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="Record_Timestamp",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]