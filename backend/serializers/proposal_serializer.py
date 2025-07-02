from rest_framework import serializers
from backend.models import Proposal
from backend.models.project import Project
from backend.serializers.project_serializer import ProjectSerializer
from backend.serializers.user_serializer import UserSerializer

class ProposalSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    file_size_formatted = serializers.ReadOnlyField()

    class Meta:
        model = Proposal
        fields = [
            'id', 'project', 'submitted_by', 'proposal_file', 'original_filename',
            'file_size', 'file_size_formatted', 'status',
            'feedback', 'reviewed_by', 'submitted_at', 'reviewed_at'
        ]

class ProposalUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading a proposal file with project association."""
    project_id = serializers.IntegerField(write_only=True)
    proposal_file = serializers.FileField()

    class Meta:
        """Serializer for uploading a proposal file with project association."""
        model = Proposal
        fields = ['project_id', 'proposal_file']

    def validate_project_id(self, value):
        """Validate that the project exists and is active."""
        try:
            project = Project.objects.get(id=value)
            return value
        except Project.DoesNotExist as exc:  # pylint: disable=no-member
            raise serializers.ValidationError("Project not found or inactive") from exc

    def validate_proposal_file(self, value):
        """Validate the uploaded proposal file."""
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 10MB")

        # Check file extension
        allowed_extensions = ['pdf', 'doc', 'docx']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            raise serializers.ValidationError(
                f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
            )

        return value

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        project = Project.objects.get(id=project_id)

        proposal = Proposal.objects.create(
            project=project,
            submitted_by=self.context['request'].user,
            original_filename=validated_data['proposal_file'].name,
            file_size=validated_data['proposal_file'].size,
            **validated_data
        )
        return proposal
