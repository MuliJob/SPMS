from rest_framework import serializers
from backend.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_reg_no = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'status', 'submitted_at', 'student_name', 'student_reg_no']

    def get_student_name(self, obj):
        return obj.student.get_full_name()

    def get_student_reg_no(self, obj):
        return obj.student.student.registration_number if hasattr(obj.student, 'student') else None
