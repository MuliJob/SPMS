from rest_framework import viewsets
from .models import User, Student, Supervisor, Project, Proposal, Announcement
from  backend.serializers import  UserSerializer, StudentSerializer, SupervisorSerializer, ProjectSerializer, ProposalSerializer, AnnouncementSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from backend.permissions.is_lecturer import IsLecturer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SupervisorViewSet(viewsets.ModelViewSet):
     queryset = Supervisor.objects.all()
     serializer_class = SupervisorSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

   