from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import ProjectTopic
from .serializers import ProjectTopicSerializer
from .permissions import IsStudent

# Create your views here.
class TopicSubmitView(generics.CreateAPIView):
    serializer_class = ProjectTopicSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        student = self.request.user
        if ProjectTopic.objects.filter(student=student).count() >= 3:
            raise ValidationError("You have reached the topic submission limit (3).")
        serializer.save(student=student)

class TopicListView(generics.ListAPIView):
    serializer_class = ProjectTopicSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Project.objects.filter(student=self.request.user)