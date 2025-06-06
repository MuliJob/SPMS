from rest_framework import viewsets, status, permissions
from .models import User, Student, Supervisor, Project, Proposal, Announcement
from  backend.serializers import  UserSerializer, StudentSerializer, SupervisorSerializer, ProjectSerializer, ProposalSerializer, AnnouncementSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from backend.permissions import IsLecturer,IsStudent, IsSupervisor
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
    permission_classes = [permisssions.IsAuthenticated]

    def perform_create(self,serializer):
        project = serializer.validated_data['project']
        if self.request.user != project.student:
            raise permissionError("You are not allowed to submit a proposal for this project.")
        serializer.save()

    @action(detail =True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSupervisor | IsLecturer])
    def add_feedback(self, request, pk=None):
        proposal =self.get_object()
        feedback = request.data.get('feedback')

        if not feedback:
            return Response({'error': 'Feedback is required'}, status=status.HTTP_400_BAD_REQUESt)
        proposal.feedback = feedback
        proposal.save()
        return Response({'message': 'Feedback added'}, status=status.HTTP_200_OK)   


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

   