from rest_framework import viewsets, status, permissions
from .models import User, Student, Supervisor, Project, Proposal, Announcement, Notification
from  backend.serializers import  UserSerializer, StudentSerializer, SupervisorSerializer, ProjectSerializer, ProposalSerializer, AnnouncementSerializer, UserSerializer, NotificationSerializer
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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        project = serializer.validated_data['project']
        if self.request.user != project.student:
            raise permissionError("You are not allowed to submit a proposal for this project.")
        serializer.save()

    @action(detail =True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSupervisor | IsLecturer])
    def add_feedback(self, request, pk=None):
        student_user = proposal.project.student
        Notification.objects.create(
    user=student_user,
    message=f"Feedback added to your proposal: '{proposal.project.title}'"
)
        proposal =self.get_object()
        feedback = request.data.get('feedback')

        if not feedback:
            return Response({'error': 'Feedback is required'}, status=status.HTTP_400_BAD_REQUEST)
        proposal.feedback = feedback
        proposal.status = 'reviewed'
        proposal.save()
        return Response({'message': 'Feedback added and status set to reviewed'}, status=status.HTTP_200_OK)   

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsSupervisor])
    def feedback(self, request, pk=None):
        proposal = self.get_object()
        user = request.user

     

        
        if proposal.project.supervisor and proposal.project.supervisor.user == user:
            feedback_text = request.data.get('feedback')
            if not feedback_text:
                return Response({'error': 'Feedback is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            proposal.feedback = feedback_text
            proposal.status = 'reviewed'
            proposal.save()
            return Response({'message': 'Feedback submitted and status set to reviewed'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not the supervisor of this project'}, status=status.HTTP_403_FORBIDDEN)



class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
   
