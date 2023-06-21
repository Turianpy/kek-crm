# Generated by Django 4.2.1 on 2023-06-20 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField()),
                ('ended_at', models.DateTimeField()),
            ],
            options={
                'ordering': ['started_at'],
            },
        ),
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.EmailField(max_length=254)),
                ('receiver', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=256)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/images')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('sender', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=256)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='interactions.chatlog')),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('phone call', 'phone call'), ('chat', 'chat'), ('email', 'email')], max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.CharField(max_length=256)),
                ('recording', models.FileField(null=True, upload_to='media/recordings')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interactions', to='customers.customer')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
