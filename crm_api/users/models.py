from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    employed_since = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING, related_name='users')


class Role(models.Model):
    name = models.CharField(max_length=30)
    permissions = models.CharField(max_length=256)

    def __str__(self):
        return self.name