# Generated by Django 4.2.1 on 2023-06-27 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0003_alter_interaction_options_alter_interaction_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emaillog',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
    ]
