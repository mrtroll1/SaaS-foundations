# Generated by Django 5.1.2 on 2024-10-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subscription",
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
                ("name", models.CharField(max_length=120)),
            ],
            options={
                "permissions": [
                    ("basic", "Basic Permission"),
                    ("pro", "Pro Permission"),
                    ("adbanced", "Advanced Permission"),
                ],
            },
        ),
    ]