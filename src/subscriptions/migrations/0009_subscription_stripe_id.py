# Generated by Django 5.1.2 on 2024-10-26 15:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0008_usersubscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="stripe_id",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]