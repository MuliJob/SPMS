from rest_framework import serializers
from backend.models import Project, Proposal




class ProjectSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_reg_no = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'submitted_at', 'student_name', 'student_reg_no']

    def get_student_name(self, obj):
        try:
            return obj.student.user.get_full_name()
        except Exception:
            return None

    def get_student_reg_no(self, obj):
        try:
            return obj.student.registration_number
        except Exception:
            return None

        try:
            return obj.student.registration_number
        except Exception:
            return None






class ProjectProposalsSerializer(serializers.ModelSerializer):
    proposals = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    student_reg_no = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'status',
            'submitted_at',
            'student_name',
            'student_reg_no',
            'proposals'
        ]

    def get_student_name(self, obj):
        try:
            return obj.student.user.get_full_name()
        except Exception:
            return None

    def get_student_reg_no(self, obj):
        try:
            return obj.student.registration_number
        except Exception:
            return None


    def get_proposals(self, obj):
        proposals = Proposal.objects.filter(project=obj)
        from backend.serializers.proposal_serializer import ProposalSerializer
        return ProposalSerializer(proposals, many=True, context=self.context).data

