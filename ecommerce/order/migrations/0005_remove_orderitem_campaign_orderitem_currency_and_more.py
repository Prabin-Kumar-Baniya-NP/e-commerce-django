# Generated by Django 4.1.5 on 2023-02-08 14:48

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_rename_product_orderitem_variant"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="campaign",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="currency",
            field=models.CharField(
                choices=[("USD", "USD")], default="USD", max_length=3
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=1,
                help_text="Price in USD",
                max_digits=10,
                validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
            ),
            preserve_default=False,
        ),
    ]
