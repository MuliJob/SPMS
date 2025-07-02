from django.db import models
from .user import User
from .supervisor import Supervisor


class Project(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='Pending' )
    supervisor = models.ForeignKey(Supervisor, null=True, blank=True, on_delete=models.SET_NULL)
    submitted_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title