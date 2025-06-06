from rest_framework import viewsets
from .models import User, Student, Supervisor, Project, Proposal, Announcement
from  backend.serializers import  UserSerializer, StudentSerializer, SupervisorSerializer, ProjectSerializer, ProposalSerializer, AnnouncementSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from backend.permissions.is_lecturer import IsLecturer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

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
    permission_classes = [IsAuthenticated]  

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsLecturer])
    def approve(self, request, pk=None):
        project = self.get_object()
        project.status = 'approved'
        project.save()
        return Response({'message': 'Project approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsLecturer])
    def reject(self, request, pk=None):
        project = self.get_object()
        project.status = 'rejected'
        project.save()
        return Response({'message': 'Project rejected'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsLecturer])
    def assign_supervisor(self, request, pk=None):
        project = self.get_object()
        supervisor_id = request.data.get('supervisor_id')
        
        if not supervisor_id:
            return Response({'error': 'Supervisor ID is required'}, status=400)

        supervisor = get_object_or_404(Supervisor, id=supervisor_id)
        project.supervisor = supervisor
        project.save()
        
        return Response({'message': f'Supervisor {supervisor.user.username} assigned successfully'}, status=200)

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

   