from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistartionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('student','student'), ('supervisor', 'supervisor')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']


    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password'],
            role= validated_data['role']
        )

        return user
