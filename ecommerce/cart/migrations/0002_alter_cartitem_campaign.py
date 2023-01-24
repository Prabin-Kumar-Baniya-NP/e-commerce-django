# Generated by Django 4.1.5 on 2023-01-24 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0002_rename_desciption_campaign_description"),
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="campaign",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="campaign",
                to="campaign.campaign",
            ),
        ),
    ]