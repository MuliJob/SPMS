from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .user_views import UserViewSet, StudentViewSet, SupervisorViewSet, ProjectViewSet, ProposalViewSet, AnnouncementViewSet, NotificationViewSet
from .views.auth import CustomAuthToken,  LogoutView
from .views.register import RegistrationView
from backend.views.login import LoginView
from backend.views.test_view import ProtectedTestView
from backend.views.dashboard import StudentDashboardView, SupervisorDashboardView, LecturerDashboardView
from backend.views.student import SubmitTopicView



router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet, basename='students')
router.register(r'supervisors', SupervisorViewSet, basename='supervisors')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'proposals', ProposalViewSet, basename='proposals')
router.register(r'announcements', AnnouncementViewSet, basename='announcements')
router.register(r'notifications', NotificationViewSet, basename='notifications')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedTestView.as_view(), name='protected'),
    path('api/auth/', include('dj_rest_auth.urls')),  
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  
    path('api/auth/social/', include('allauth.socialaccount.urls')),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('dashboard/supervisor/', SupervisorDashboardView.as_view(), name='supervisor-dashboard'),
    path('dashboard/lecturer/', LecturerDashboardView.as_view(), name='lecturer-dashboard'),
    path('dashboard/student/submit-topic/', SubmitTopicView.as_view(), name='submit-topic'),



]


