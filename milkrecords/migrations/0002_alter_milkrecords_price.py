# Generated by Django 5.1.1 on 2024-10-31 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milkrecords', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milkrecords',
            name='price',
            field=models.SmallIntegerField(default=70),
        ),
    ]
