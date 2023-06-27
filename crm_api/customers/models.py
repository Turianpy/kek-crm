from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    business = models.ForeignKey(
        'Business',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='representatives')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Business(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.name
