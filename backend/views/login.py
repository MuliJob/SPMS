from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from backend.serializers.user_serializer import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)


    

        if user:
            print("Authenticated user:", user)
            print("User role:", user.role)

            token, _ = Token.objects.get_or_create(user=user)
            

            return Response({
                "message": "Login successful",
                "user": UserSerializer(user).data,
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "role": user.role  

            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Invalid username or password"
            }, status=status.HTTP_401_UNAUTHORIZED)
