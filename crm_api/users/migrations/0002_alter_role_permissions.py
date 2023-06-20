# Generated by Django 4.2.1 on 2023-06-20 08:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('create interactions', 'create interactions'), ('view interactions', 'view interactions'), ('create customers', 'create customers'), ('view customers', 'view customers'), ('create users', 'create users'), ('view logs', 'view logs'), ('view other users', 'view other users'), ('admin', 'admin')], max_length=30), size=None),
        ),
    ]
