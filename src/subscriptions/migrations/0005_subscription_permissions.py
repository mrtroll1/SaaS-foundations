# Generated by Django 5.1.2 on 2024-10-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("subscriptions", "0004_alter_subscription_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="permissions",
            field=models.ManyToManyField(to="auth.permission"),
        ),
    ]
