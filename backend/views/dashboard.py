from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsStudent, IsSupervisor, IsLecturer
from backend.models import Project, Proposal, Supervisor, Student, User


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user
        projects = Project.objects.filter(student=student)
        project = projects.first()
        proposal_submitted = Proposal.objects.filter(project__student=student).exists()
        return Response({
            'projects_submitted': projects.count(),
            'proposal_submitted': proposal_submitted,
            'project_status': project.status if project else 'No project'
        })



class SupervisorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request):
        supervisor = Supervisor.objects.get(user=request.user)
        supervised_projects = Project.objects.filter(supervisor=supervisor)
        proposals = Proposal.objects.filter(project__in=supervised_projects)
        feedback_given = proposals.exclude(feedback__isnull=True).count()

        return Response({
            'supervised_students': supervised_projects.count(),
            'received_proposals': proposals.count(),
            'feedback_given': feedback_given
        })



class LecturerDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def get(self, request):
        pending = Project.objects.filter(status='pending').count()
        approved = Project.objects.filter(status='approved').count()
        students = Student.objects.count()

        return Response({
            'pending_projects': pending,
            'approved_projects': approved,
            'total_students': students
        })
