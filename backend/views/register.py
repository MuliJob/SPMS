from rest_framework.views import APIView
from rest_framework.response import response
from rest_framework import status
from backend.serializers.user_registration_serializer import UserRegistrationSerializer


class RegistartionView(APIView):
    def post(self, request):
        serializer =UserRegistartionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            