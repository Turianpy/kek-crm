from django.contrib.postgres import fields as f
from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    business = models.ForeignKey(
        'Business',
        on_delete=models.DO_NOTHING,
        null=True)

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
