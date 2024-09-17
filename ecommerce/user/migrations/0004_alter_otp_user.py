# Generated by Django 5.0.6 on 2024-09-17 21:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_otp_email_otp_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="otp",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="otp",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
