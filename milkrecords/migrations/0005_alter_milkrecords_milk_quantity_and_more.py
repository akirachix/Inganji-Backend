# Generated by Django 4.2.16 on 2024-11-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("milkrecords", "0004_merge_20241117_1230"),
    ]

    operations = [
        migrations.AlterField(
            model_name="milkrecords",
            name="milk_quantity",
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name="milkrecords",
            name="price",
            field=models.SmallIntegerField(default=70),
        ),
    ]