# Generated by Django 4.2.16 on 2024-11-06 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("predictive_model", "0004_rename_farmer_prediction_farmer_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="prediction",
            old_name="farmer_id",
            new_name="farmer",
        ),
    ]