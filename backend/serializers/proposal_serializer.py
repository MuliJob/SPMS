from rest_framework import serializers
from backend.models import Proposal

class ProposalSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Proposal
        fields = ['id', 'project', 'file', 'file_url', 'feedback', 'submitted_at', 'status']

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url) if obj.file else None
