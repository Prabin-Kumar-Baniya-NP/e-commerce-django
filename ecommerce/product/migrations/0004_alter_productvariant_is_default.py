# Generated by Django 4.1.5 on 2023-03-01 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_productvariant_is_default"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productvariant",
            name="is_default",
            field=models.BooleanField(default=False),
        ),
    ]
