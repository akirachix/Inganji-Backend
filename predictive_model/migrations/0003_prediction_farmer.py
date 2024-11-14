# Generated by Django 4.2.16 on 2024-11-05 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("farmers", "0008_remove_farmersmanagement_sacco_name_and_more"),
        ("predictive_model", "0002_remove_prediction_household_size_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="prediction",
            name="farmer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="farmers.farmersmanagement",
            ),
        ),
    ]