from rest_framework import serializers
from backend.models import Supervisor



class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'

class SupervisorListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Supervisor
        fields = ['id', 'name']

    def get_name(self, obj):
        full_name = obj.user.get_full_name()
        return full_name if full_name.strip() else obj.user.username
