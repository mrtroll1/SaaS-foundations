# Generated by Django 5.1.2 on 2024-10-27 13:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "subscriptions",
            "0014_alter_subscription_options_subscription_featured_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscriptionprice",
            options={
                "ordering": ["subscription__order", "order", "featured", "-updated"]
            },
        ),
    ]