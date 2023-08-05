# Generated by Django 4.2.1 on 2023-07-05 10:52

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0005_alter_emaillog_options_alter_image_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='body',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='sent_at',
        ),
        migrations.RemoveField(
            model_name='emaillog',
            name='subject',
        ),
        migrations.AddField(
            model_name='emaillog',
            name='participants',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), default=['kek@kek.kek'], size=None),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.EmailField(max_length=254)),
                ('receiver', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField()),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='interactions.emaillog')),
            ],
        ),
    ]