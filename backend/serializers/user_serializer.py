import requests
from django.contrib.auth import get_user_model
from rest_framework import serializers
from backend.models import Student, Supervisor, Lecturer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[('student', 'student'), ('supervisor', 'supervisor'), ('lecturer', 'lecturer')])

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone_number',
                 'profile_picture', 'is_email_verified', 'created_at', 'password']
        read_only_fields = ['id', 'created_at', 'is_email_verified']

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        user.role = role
        user.save()

        if role == 'student':
            Student.objects.create(user=user, registration_number=f"REG-{user.id}")
        elif role == 'supervisor':
            Supervisor.objects.create(user=user)
        elif role == 'lecturer':
            Lecturer.objects.create(user=user)

        return user

class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    
    def validate_access_token(self, access_token):
        """Validate Google access token"""
        
        # Verify token with Google
        response = requests.get(
            f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}',
            timeout=5
        )

        print(f'Status Code: {response.status_code}')
        print(f'Response Body: {response.json()}')

        if response.status_code != 200:
            raise serializers.ValidationError('Invalid access token')
        
        return access_token

    def create(self, validated_data):
        # No-op implementation for abstract method
        return validated_data

    def update(self, instance, validated_data):
        # No-op implementation for abstract method
        return instance