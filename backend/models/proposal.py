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
        if self.file_size is None:
            return "Unknown"
    
        size = float(self.file_size)
        if size < 1024.0:
            return f"{size:.1f} B"
        elif size < 1024.0**2:
            return f"{size/1024.0:.1f} KB"
        elif size < 1024.0**3:
             return f"{size/(1024.0**2):.1f} MB"
        else:
            return f"{size/(1024.0**3):.1f} GB"

    class Meta:
        """Meta options for the Proposal model."""
        ordering = ['-submitted_at']
