# Generated by Django 4.1.5 on 2023-01-26 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0018_alter_productvariant_product"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="productvariant",
            options={"ordering": ["price"]},
        ),
        migrations.RemoveField(
            model_name="productvariant",
            name="is_default",
        ),
    ]
