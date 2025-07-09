from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from backend.models import Project, Proposal
from backend.serializers.project_serializer import ProjectSerializer
from backend.serializers.proposal_serializer import ProposalSerializer
from backend.permissions import IsSupervisor
from rest_framework import status
from backend.serializers.project_serializer import ProjectProposalsSerializer



class AssignedProjectsView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request):
        supervisor = getattr(request.user, 'supervisor', None)
        if supervisor is None:
            return Response({'detail': 'Supervisor profile not found.'}, status=400)

        assigned_projects = Project.objects.filter(supervisor=supervisor)

        serializer = ProjectProposalsSerializer(assigned_projects, many=True, context={'request': request})

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


class ProposalApprovalView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def post(self, request, proposal_id, action):
        try:
            proposal = Proposal.objects.get(id=proposal_id)
            if proposal.project.supervisor.user != request.user:
                return Response({'detail': 'Not authorized'}, status=403)

            if action == 'approve':
                proposal.status = 'approved'
            elif action == 'reject':
                proposal.status = 'rejected'
            else:
                return Response({'detail': 'Invalid action'}, status=400)

            proposal.save()
            return Response({'message': f'Proposal {action}d successfully.'})
        except Proposal.DoesNotExist:
            return Response({'detail': 'Proposal not found'}, status=404)



class ProjectProposalsView(APIView):
    permission_classes = [IsAuthenticated, IsSupervisor]

    def get(self, request, project_id):
        user = request.user
        supervisor = getattr(user, 'supervisor', None)

        try:
            project = Project.objects.get(id=project_id, supervisor=supervisor)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found or not assigned to you."}, status=404)

        proposals = Proposal.objects.filter(project=project)
        serializer = ProposalSerializer(proposals, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)