# Generated by Django 5.1.6 on 2025-03-08 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_user_phone_number_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
