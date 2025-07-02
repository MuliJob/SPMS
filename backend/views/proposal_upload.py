"""Proposal upload view for handling proposal submissions."""
import logging
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication

from backend.serializers.proposal_serializer import ProposalSerializer, ProposalUploadSerializer


logger = logging.getLogger(__name__)

class ProposalUploadView(generics.CreateAPIView):
    serializer_class = ProposalUploadSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        logger.info(f"Proposal upload attempt by user: {request.user.username}")
        logger.info(f"Request data: {request.data}")
        logger.info(f"Request files: {request.FILES}")

        try:
            # Inject project_id from URL into request.data
            project_id = kwargs.get('project_id')
            mutable_data = request.data.copy()
            mutable_data['project'] = project_id

            serializer = self.get_serializer(data=mutable_data)
            if serializer.is_valid():
                proposal = serializer.save()
                logger.info(f"Proposal uploaded successfully: {proposal.id}")

                response_serializer = ProposalSerializer(proposal)
                return Response(
                    {
                        'message': 'Proposal uploaded successfully',
                        'proposal': response_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                logger.error(f"Proposal upload validation failed: {serializer.errors}")
                return Response(
                    {
                        'error': 'Validation failed',
                        'details': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Proposal upload error: {str(e)}", exc_info=True)
            return Response(
                {
                    'error': 'Internal server error',
                    'detail': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
