# Generated by Django 5.1.2 on 2024-10-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0019_rename_stripe_id_usersubscription_sub_stripe_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersubscription",
            name="user_cancelled",
            field=models.BooleanField(default=False),
        ),
    ]
