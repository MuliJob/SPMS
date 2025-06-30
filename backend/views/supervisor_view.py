from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import Project
from backend.serializers.project_serializer import ProjectSerializer
from backend.permissions import IsSupervisor

class AssignedProjectsView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request):
        user = request.user
        supervisor = user.supervisor

        assigned_projects = Project.objects.filter(supervisor=supervisor)
        serializer = ProjectSerializer(assigned_projects, many=True)

        return Response(serializer.data)
