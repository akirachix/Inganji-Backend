# Generated by Django 4.2.16 on 2024-09-27 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cooperative", "0002_cooperative_user"),
        ("sacco", "0002_sacco_user"),
        ("farmers", "0007_alter_farmersmanagement_cooperative_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="farmersmanagement",
            name="sacco_name",
        ),
        migrations.AddField(
            model_name="farmersmanagement",
            name="sacco_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sacco",
                to="sacco.sacco",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="farmersmanagement",
            name="cooperative_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cooperative",
                to="cooperative.cooperative",
            ),
        ),
    ]
