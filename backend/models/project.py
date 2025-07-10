from django.db import models
from .user import User
from .supervisor import Supervisor


class Project(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='Pending' )
    supervisor = models.ForeignKey('Supervisor', on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

   