# Generated by Django 4.2.16 on 2024-09-27 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cooperative", "0002_cooperative_user"),
        ("farmers", "0006_alter_farmersmanagement_cooperative_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farmersmanagement",
            name="cooperative_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="farmers",
                to="cooperative.cooperative",
            ),
        ),
    ]
