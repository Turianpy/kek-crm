# Generated by Django 4.2.1 on 2023-07-05 10:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0006_remove_emaillog_body_remove_emaillog_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaillog',
            name='participants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), null=True, size=None),
        ),
    ]
