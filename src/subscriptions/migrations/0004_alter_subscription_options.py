# Generated by Django 5.1.2 on 2024-10-25 18:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0003_alter_subscription_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscription",
            options={
                "permissions": [
                    ("basic", "Basic Permission"),
                    ("pro", "Pro Permission"),
                    ("adbanced", "Advanced Permission"),
                    ("basic_ai", "Basic AI Permission"),
                ]
            },
        ),
    ]
