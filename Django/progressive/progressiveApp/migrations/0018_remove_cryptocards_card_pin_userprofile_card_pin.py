# Generated by Django 5.0.2 on 2024-03-04 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0017_rename_pin_cryptocards_card_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cryptocards',
            name='card_pin',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='card_pin',
            field=models.IntegerField(default=0),
        ),
    ]