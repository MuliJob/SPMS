from rest_framework import serializers
from backend.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_reg_no = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'submitted_at', 'student_name', 'student_reg_no']

    def get_student_name(self, obj):
        try:
            return obj.student.get_full_name() or obj.student.username
        except AttributeError:
            return obj.student.username if obj.student else None

    def get_student_reg_no(self, obj):
        user = obj.student
        try:
            return user.student.registration_number
        except AttributeError:
            return None
        except user._meta.model.student.RelatedObjectDoesNotExist:
            return None




class ProjectWithProposalsSerializer(serializers.ModelSerializer):
    proposals = ProjectSerializer(many=True, read_only=True)
    student_name = serializers.SerializerMethodField()
    student_reg_no = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'status', 'submitted_at',
            'student_name', 'student_reg_no', 'proposals',
        ]

    def get_student_name(self, obj):
        try:
            return obj.student.student.full_name
        except Exception:
            return ""

    def get_student_reg_no(self, obj):
        try:
            return obj.student.student.registration_number
        except Exception:
            return ""
