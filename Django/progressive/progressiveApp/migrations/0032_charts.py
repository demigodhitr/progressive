# Generated by Django 5.0.2 on 2024-03-14 16:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progressiveApp', '0031_alter_userprofile_accountmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('deposits', models.CharField(blank=True, default='Deposits', editable=False, max_length=10, verbose_name='deposits')),
                ('deposits_day_one', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('deposits_day_two', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('deposits_day_three', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('deposits_day_four', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('deposits_day_five', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('profits', models.CharField(blank=True, default='Profits', editable=False, max_length=10, verbose_name='profits')),
                ('profits_day_one', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('profits_day_two', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('profits_day_three', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('profits_day_four', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('profits_day_five', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('losses', models.CharField(blank=True, default='Profits', editable=False, max_length=10, verbose_name='losses')),
                ('losses_day_one', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('losses_day_two', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('losses_day_three', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('losses_day_four', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('losses_day_five', models.CharField(blank=True, default=0, max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
