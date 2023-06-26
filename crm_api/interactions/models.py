from customers.models import Customer
from django.db import models
from users.models import User

INTERACTION_TYPES = [
    ("phone call", "phone call"),
    ("chat", "chat"),
    ("email", "email")
]


class Interaction(models.Model):
    type = models.CharField(choices=INTERACTION_TYPES, max_length=30)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.DO_NOTHING,
        related_name='interactions'
    )
    date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='interactions')
    recording = models.FileField(upload_to='media/recordings', null=True)

    class Meta:
        ordering = ['-date']


class ChatLog(models.Model):
    interaction = models.ForeignKey(
        Interaction,
        on_delete=models.CASCADE,
        related_name='chatlog'
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()

    class Meta:
        ordering = ['started_at']


class Message(models.Model):
    timestamp = models.DateTimeField()
    sender = models.CharField(max_length=30)
    content = models.CharField(max_length=256)
    chat = models.ForeignKey(
        ChatLog,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    class Meta:
        ordering = ['timestamp']


class Image(models.Model):
    image = models.ImageField(upload_to='media/images')
    interaction = models.ForeignKey(
        Interaction,
        on_delete=models.CASCADE,
        related_name='images'
    )


class EmailLog(models.Model):
    interaction = models.ForeignKey(
        Interaction,
        on_delete=models.CASCADE,
        related_name='emaillog'
    )
    sender = models.EmailField()
    receiver = models.EmailField()
    subject = models.CharField(max_length=256)
    body = models.TextField()
    sent_at = models.DateTimeField()
