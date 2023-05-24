from django.db import models
from django.contrib.postgres import fields as f


class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
