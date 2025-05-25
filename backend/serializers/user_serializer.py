from django.contrib.auth import get_user_model
from rest_framework import serializers
from backend.models import Student, Supervisor



User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('student','student'), ('supervisor', 'supervisor')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']


    def  create(self, validated_data):
        role = validated_data.get('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )

        
        if role == 'student':
            Student.objects.create(user=user, registration_number=f"REG-{user.id}")
        elif role == 'supervisor':
            Supervisor.objects.create(user=user)

        return user