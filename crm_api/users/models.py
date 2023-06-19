from django.contrib.auth.models import AbstractUser
from django.contrib.postgres import fields as f
from django.db import models

USER_PERMISSIONS = (
    ('create interactions', 'create interactions'),
    ('view interactions', 'view interactions'),
    ('create customers', 'create customers'),
    ('view customers', 'view customers'),
    ('create users', 'create users'),
    ('view logs', 'view logs'),
    ('view other users', 'view other users'),
    ('admin', 'admin')
)


class User(AbstractUser):
    employed_since = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    role = models.ForeignKey(
        'Role',
        on_delete=models.DO_NOTHING,
        related_name='users'
    )

    @property
    def is_admin(self):
        return (
            self.role.name == 'admin' or 'admin' in self.role.permissions
            ) or self.is_staff


class Role(models.Model):
    name = models.CharField(max_length=30)
    permissions = f.ArrayField(models.CharField(choices=USER_PERMISSIONS))

    def __str__(self):
        return self.name
