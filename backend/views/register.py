from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend.serializers.user_serializer import UserSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer =UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            