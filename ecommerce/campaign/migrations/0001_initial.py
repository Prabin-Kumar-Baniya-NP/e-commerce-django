# Generated by Django 4.1.5 on 2023-02-14 08:55

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(max_length=1024)),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Value in percentage",
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00"))
                        ],
                    ),
                ),
                ("start_datetime", models.DateTimeField()),
                ("end_datetime", models.DateTimeField()),
                ("promocode", models.CharField(max_length=16)),
                ("auto_apply", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "product",
                    models.ManyToManyField(
                        related_name="product_promotion", to="product.product"
                    ),
                ),
            ],
        ),
    ]
