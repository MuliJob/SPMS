from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
        ('lecturer', 'Lecturer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Student(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    registartion_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.user.username

class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Project(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='Pending' )
    supervisor = models.ForeignKey(Supervisor, null=True, blank=True, on_delete=models.SET_NULL)
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Proposal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    document = models.FileField(upload_to='proposals/')
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"proposal for {self.project.title}"


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement by {self.author.username} on {self.created_at.date()}"

