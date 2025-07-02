from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import Project, Proposal
from backend.serializers.project_serializer import ProjectSerializer
from backend.serializers.proposal_serializer import ProposalSerializer
from backend.permissions import IsSupervisor

class AssignedProjectsView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request):
        user = request.user
        supervisor = user.supervisor

        assigned_projects = Project.objects.filter(supervisor=supervisor)
        serializer = ProjectSerializer(assigned_projects, many=True)

        return Response(serializer.data)


class SupervisorProposalListView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request):
        supervisor = request.user.supervisor
        proposals = Proposal.objects.filter(project__supervisor=supervisor).order_by('-submitted_at')
        serializer = ProposalSerializer(proposals, many=True, context={'request': request})
        return Response(serializer.data)


class ProposalFeedbackView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, proposal_id):
        try:
            proposal = Proposal.objects.get(id=proposal_id, project__supervisor=request.user.supervisor)
        except Proposal.DoesNotExist:
            return Response({"detail": "Proposal not found or unauthorized."}, status=404)

        feedback = request.data.get('feedback')
        if not feedback:
            return Response({"detail": "Feedback is required."}, status=400)

        proposal.feedback = feedback
        proposal.status = "reviewed"
        proposal.save()

        return Response({"message": "Feedback added and proposal marked as reviewed."}, status=200)


class ApproveProposalView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, proposal_id):
        try:
            proposal = Proposal.objects.get(id=proposal_id, project__supervisor=request.user.supervisor)
        except Proposal.DoesNotExist:
            return Response({"detail": "Proposal not found or unauthorized."}, status=404)

        proposal.status = "approved"
        proposal.save()

        return Response({"message": "Proposal approved."}, status=200)


class RejectProposalView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, proposal_id):
        try:
            proposal = Proposal.objects.get(id=proposal_id, project__supervisor=request.user.supervisor)
        except Proposal.DoesNotExist:
            return Response({"detail": "Proposal not found or unauthorized."}, status=404)

        proposal.status = "rejected"
        proposal.save()

        return Response({"message": "Proposal rejected."}, status=200)
