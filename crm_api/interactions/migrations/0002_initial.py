# Generated by Django 4.2.1 on 2023-06-20 15:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('interactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='image',
            name='interaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='interactions.interaction'),
        ),
        migrations.AddField(
            model_name='emaillog',
            name='interaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emaillog', to='interactions.interaction'),
        ),
        migrations.AddField(
            model_name='chatlog',
            name='interaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatlog', to='interactions.interaction'),
        ),
    ]
