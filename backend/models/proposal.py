from django.db import models
from .project import Project


def proposal_upload_path(instance, filename):
    return f'proposals/student_{instance.project.student.id}/{filename}'


class Proposal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to=proposal_upload_path)
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"proposal for - {self.project.title}"

