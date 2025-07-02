from django.db import models
from .user import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    registration_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.registration_number})"
