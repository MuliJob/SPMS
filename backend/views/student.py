from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.models import Project, Student
from rest_framework import status
from backend.serializers import ProjectSerializer 

class SubmitTopicView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')

        try:
            student = request.user.student  

            
            if Project.objects.filter(student=student).exists():
                return Response({"error": "You have already submitted a topic."}, status=status.HTTP_400_BAD_REQUEST)

        
            Project.objects.create(
                student=student,
                title=title,
                description=description,
                status='pending'
            )
            return Response({"message": "Project topic submitted successfully."}, status=status.HTTP_201_CREATED)

        except Student.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)