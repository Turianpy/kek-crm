# Generated by Django 4.2.1 on 2023-06-26 14:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interactions', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interaction',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='interaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interactions', to=settings.AUTH_USER_MODEL),
        ),
    ]
