from django.urls import path, include
from rest_framework import DefaultRouter
from .views import UserViewSet, StudentViewSet, SupervisorViewSet, ProjectViewSet, ProposalViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'supervisors', SupervisorViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'proposals', ProposalViewSet)
router.register(r'announcements', AnnouncementViewSet)

urlpatterns = [
    path('api/students/', include(router.urls)),
]
