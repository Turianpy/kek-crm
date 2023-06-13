from django.db import models
from django.contrib.postgres import fields as f


class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    business = models.ForeignKey('Business', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
