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
        fields = ['username', 'email', 'password', 'role']

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
