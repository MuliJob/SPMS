from rest_framework import serializers
from backend.models import Supervisor

class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'
