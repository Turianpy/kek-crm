from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    employed_since = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)

    @property
    def is_admin(self):
        return (
            'admin' in self.groups.values_list('name', flat=True)
            or self.is_superuser
        )

    @property
    def is_staff(self):
        return (
            self.is_admin
            or 'manager' in self.groups.values_list('name', flat=True)
        )

    def has_perm(self, perm: str, obj=None) -> bool:
        return super().has_perm(perm, obj) or self.is_admin
