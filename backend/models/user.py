from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
        ('lecturer', 'Lecturer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
