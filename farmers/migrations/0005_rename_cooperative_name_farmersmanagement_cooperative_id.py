# Generated by Django 5.1.1 on 2024-09-26 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0004_remove_farmersmanagement_cooperative_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='farmersmanagement',
            old_name='cooperative_name',
            new_name='cooperative_id',
        ),
    ]