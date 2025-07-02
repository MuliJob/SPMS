from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.models import Project, Supervisor
from backend.serializers.project_serializer import ProjectSerializer
from backend.permissions import IsLecturer  
from rest_framework import status
from backend.serializers.supervisor_serializer import SupervisorListSerializer


class SubmittedTopicsView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def get(self, request):
        topics = Project.objects.all().order_by('-submitted_at')
        serializer = ProjectSerializer(topics, many=True)
        return Response(serializer.data)

class ApproveTopicView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.status = 'approved'
            project.save()
            return Response({'message': 'Project approved'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class RejectTopicView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.status = 'rejected'
            project.save()
            return Response({'message': 'Project rejected'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class AssignSupervisorView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request, pk):
        supervisor_id = request.data.get('supervisor_id')
        if not supervisor_id:
            return Response({"error": "Supervisor ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            supervisor = Supervisor.objects.get(pk=supervisor_id)
        except Supervisor.DoesNotExist:
            return Response({"error": "Supervisor not found"}, status=status.HTTP_404_NOT_FOUND)

        project.supervisor = supervisor
        project.save()

        return Response({
            "message": "Supervisor assigned successfully",
            "project": project.title,
            "supervisor": str(supervisor)
        }, status=status.HTTP_200_OK)


class SupervisorListView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def get(self, request):
        supervisors = Supervisor.objects.all()
        serializer = SupervisorListSerializer(supervisors, many=True)
        return Response(serializer.data)