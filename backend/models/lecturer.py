from django.db import models
from backend.models.user import User


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Lecturer: {self.user.username}"
