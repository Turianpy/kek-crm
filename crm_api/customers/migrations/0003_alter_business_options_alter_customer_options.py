# Generated by Django 4.2.1 on 2023-06-27 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_business'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
    ]
