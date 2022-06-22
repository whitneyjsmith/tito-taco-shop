from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

def creation_date():
    return date.today()


class User(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField()
    creation_date = models.DateField(default=creation_date)
    is_active = models.BooleanField(default=True)
    unique_id = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'unique_id'],
                name='Taco Shop User Model'
            )
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.email}'
