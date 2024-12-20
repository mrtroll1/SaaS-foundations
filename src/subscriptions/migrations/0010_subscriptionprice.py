# Generated by Django 5.1.2 on 2024-10-26 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0009_subscription_stripe_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubscriptionPrice",
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
                ("stripe_id", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "interval",
                    models.CharField(
                        choices=[("month", "Monthly"), ("year", "Yearly")],
                        default="month",
                        max_length=30,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=99.99, max_digits=5),
                ),
                (
                    "subscription",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="subscriptions.subscription",
                    ),
                ),
            ],
        ),
    ]
