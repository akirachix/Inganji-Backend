# Generated by Django 4.2.16 on 2024-09-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmersmanagement',
            name='cooperative_number',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, unique=True),
        ),
    ]