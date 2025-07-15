from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.views.proposal_upload import ProposalUploadView
from .user_views import UserViewSet, StudentViewSet, SupervisorViewSet, ProjectViewSet, ProposalViewSet, AnnouncementViewSet, NotificationViewSet
from .views.auth import CustomAuthToken,  LogoutView
from .views.register import RegistrationView
from backend.views.login import GoogleAuthView, LoginView
from backend.views.test_view import ProtectedTestView
from backend.views.dashboard import StudentDashboardView, SupervisorDashboardView, LecturerDashboardView
from backend.views.student import SubmitTopicView
from backend.views.lecturer import SubmittedTopicsView
from backend.views.lecturer import ApproveTopicView, RejectTopicView, AssignSupervisorView
from backend.views.lecturer import SupervisorListView
from backend.views.supervisor_view import AssignedProjectsView, SupervisorProposalListView
from backend.views.supervisor_view import ProposalFeedbackView, ApproveProposalView, RejectProposalView, ProjectProposalsView





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
    path('google/', GoogleAuthView.as_view(), name='google_auth'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedTestView.as_view(), name='protected'),
    path('auth/', include('dj_rest_auth.urls')),  
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('dashboard/supervisor/', SupervisorDashboardView.as_view(), name='supervisor-dashboard'),
    path('dashboard/lecturer/', LecturerDashboardView.as_view(), name='lecturer-dashboard'),
    path('dashboard/student/submit-topic/', SubmitTopicView.as_view(), name='submit-topic'),
    path('lecturer/submitted-topics/', SubmittedTopicsView.as_view(), name='lecturer-submitted-topics'),
    path('lecturer/topic/<int:pk>/approve/', ApproveTopicView.as_view(), name='approve-topic'),
    path('lecturer/topic/<int:pk>/reject/', RejectTopicView.as_view(), name='reject-topic'),
    path('lecturer/topic/<int:pk>/assign-supervisor/', AssignSupervisorView.as_view(), name='assign-supervisor'),
    path('lecturer/supervisors/', SupervisorListView.as_view(), name='supervisor-list'),
    path('supervisor/assigned-projects/', AssignedProjectsView.as_view()),
    path('supervisor/proposals/', SupervisorProposalListView.as_view(), name='supervisor-proposals'),
    path('supervisor/proposals/', SupervisorProposalListView.as_view()),
    path('projects/<int:project_id>/proposals', ProposalUploadView.as_view(), name='proposal-upload'),
    path('supervisor/proposals/<int:proposal_id>/feedback/', ProposalFeedbackView.as_view()),
    path('supervisor/proposals/<int:proposal_id>/approve/', ApproveProposalView.as_view()),
    path('supervisor/proposals/<int:proposal_id>/reject/', RejectProposalView.as_view()),
    path('api/proposals/' , ProposalViewSet.as_view({'get': 'list', 'post': 'create'}), name='proposal-list-create'),
    path('supervisor/project/<int:project_id>/proposals/', ProjectProposalsView.as_view(), name='project-proposals'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


