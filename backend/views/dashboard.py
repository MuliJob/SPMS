from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.permissions import IsStudent, IsSupervisor, IsLecturer
from backend.models import Project, Proposal, Supervisor, Student, User


class StudentDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, 'student'):
            proposals = Proposal.objects.filter(student=user.student).values('title', 'status', 'submitted_at')
            notifications = Notification.objects.filter(user=user, is_read=False).values('message', 'created_at')

            return Response({
                "proposals": list(proposals),
                "notifications": list(notifications),
                "registration_number": user.student.registration_number,
                "full_name": user.get_full_name(),
            })
        return Response({"error": "You are not a student"}, status=403)




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
