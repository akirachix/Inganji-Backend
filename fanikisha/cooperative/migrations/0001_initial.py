# Generated by Django 5.1.1 on 2024-09-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('cooperative_id', models.AutoField(primary_key=True, serialize=False)),
                ('cooperative_name', models.CharField(max_length=255)),
            ],
        ),
    ]
