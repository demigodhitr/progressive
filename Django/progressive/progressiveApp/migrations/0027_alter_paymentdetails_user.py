# Generated by Django 5.0.2 on 2024-03-06 15:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0026_alter_cryptobalances_bitcoin_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
