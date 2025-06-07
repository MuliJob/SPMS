from rest_framework import serializers
from backend.models import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['id', 'project', 'file', 'feedback', 'submitted_at', 'status']
        read_only_fields = ['status']

