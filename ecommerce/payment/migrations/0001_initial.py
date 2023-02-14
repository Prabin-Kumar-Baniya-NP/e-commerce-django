# Generated by Django 4.1.5 on 2023-02-14 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                (
                    "provider",
                    models.CharField(choices=[("STRIPE", "STRIPE")], max_length=32),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("REQUESTED", "REQUESTED"),
                            ("FAILED", "FAILED"),
                            ("COMPLETED", "COMPLETED"),
                        ],
                        default="REQUESTED",
                        max_length=32,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="payment",
                        to="order.order",
                    ),
                ),
            ],
        ),
    ]
