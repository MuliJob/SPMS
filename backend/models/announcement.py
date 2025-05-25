from django.db import models
from .user import User

class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement by {self.author.username} at  {self.created_at.strftime('%Y-%m-%d %H:%M')}"

