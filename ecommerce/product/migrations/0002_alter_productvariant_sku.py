# Generated by Django 4.1.5 on 2023-02-25 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productvariant",
            name="sku",
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
