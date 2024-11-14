# Generated by Django 4.2.16 on 2024-11-13 14:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmers", "0008_remove_farmersmanagement_sacco_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farmersmanagement",
            name="phone_number",
            field=models.CharField(
                max_length=15,
                validators=[
                    django.core.validators.RegexValidator(
                        "^\\+250\\d{9}$",
                        "Phone number must be in the format +250XXXXXXXXX (Rwandan number format)",
                    )
                ],
            ),
        ),
    ]