# Generated by Django 5.1.1 on 2024-09-26 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0002_cooperative_user'),
        ('farmers', '0003_farmersmanagement_cooperative_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmersmanagement',
            name='cooperative_id',
        ),
        migrations.AddField(
            model_name='farmersmanagement',
            name='cooperative_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cooperative.cooperative'),
            preserve_default=False,
        ),
    ]