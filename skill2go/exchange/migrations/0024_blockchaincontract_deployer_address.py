# Generated by Django 5.1.4 on 2025-03-26 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0023_userprofile_ethereum_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockchaincontract',
            name='deployer_address',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
