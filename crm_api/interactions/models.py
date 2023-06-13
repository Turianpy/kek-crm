from django.db import models
from django.contrib.postgres import fields as f
from customers.models import Customer
from users.models import User


INTERACTION_TYPES = [
    ("phone call", "phone call"),
    ("chat", "chat"),
    ("email", "email")
]


class Interaction(models.Model):
    type = models.CharField(choices=INTERACTION_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    recording = models.FileField(upload_to='media/recordings')


class ChatLog(models.Model):
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()


class Message(models.Model):
    timestamp = models.DateTimeField()
    sender = models.CharField(max_length=30)
    content = models.CharField(max_length=256)
    chat = models.ForeignKey(ChatLog, on_delete=models.CASCADE)


class Image(models.Model):
    image = models.ImageField(upload_to='media/images')
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE)


class EmailLog(models.Model):
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE)
    sender = models.EmailField()
    receiver = models.EmailField()
    subject = models.CharField(max_length=256)
    body = models.TextField()
    sent_at = models.DateTimeField()
