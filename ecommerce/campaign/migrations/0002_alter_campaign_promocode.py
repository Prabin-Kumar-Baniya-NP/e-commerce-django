# Generated by Django 4.1.5 on 2023-02-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="promocode",
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
