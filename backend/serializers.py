from rest_framework import serializers
from .models import User, Student, Supervisor, Project, Proposal, Announcement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class StudentSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True)


    class Meta:
        model = Student
        fields = '__all__'

class SupervisorSerializer(serializers.ModelSerializer):
    User = UserSerializer(read_only=True)

    class Meta:
        model = Supervisor
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    Student = StudentSerializer(read_only=True)
    Supervisor = SupervisorSerializer(read_only=True)


    class Meta:
        model = Project
        fields = '__all__'

class ProposalSerializer(serializers.ModelSerializer):
    Project = ProjectSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    author =UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'