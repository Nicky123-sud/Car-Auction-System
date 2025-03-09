# Generated by Django 5.1.6 on 2025-02-28 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_bidder',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_seller',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('seller', 'seller'), ('bidder', 'bidder')], default='bidder', max_length=10),
        ),
    ]
