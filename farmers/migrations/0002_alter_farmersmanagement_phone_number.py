# Generated by Django 4.2.16 on 2024-09-23 08:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="farmersmanagement",
            name="phone_number",
            field=models.CharField(
                max_length=15,
                validators=[
                    django.core.validators.RegexValidator(
                        "^\\d+$", "Phone number must be numeric"
                    )
                ],
            ),
        ),
    ]