# Generated by Django 5.0.2 on 2024-03-07 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0028_alter_idme_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idme',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
