from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth import get_user_model
from .project import Project


User = get_user_model()

def proposal_upload_path(instance, filename):
    """Generate a file upload path for project proposals."""
    return f'proposals/student_{instance.project.student.id}/{filename}'


class Proposal(models.Model):
    """Model to represent a project proposal."""
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('reviewed', 'Reviewed'),
        ('needs_revision', 'Needs Revision'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="proposals", null=True, blank=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='submitted_proposals', null=True, blank=True)
    proposal_file = models.FileField(
        upload_to=proposal_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text='Upload PDF, DOC, or DOCX files only',
        null=True,
        blank=True
    )
    original_filename = models.CharField(max_length=255, null=True, blank=True)
    file_size = models.PositiveIntegerField(help_text='File size in bytes',
                                            null=True,
        blank=True)
    feedback = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_proposals'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"proposal for - {self.project.title}"

    @property
    def file_size_formatted(self):
        """Return human-readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    class Meta:
        """Meta options for the Proposal model."""
        ordering = ['-submitted_at']
