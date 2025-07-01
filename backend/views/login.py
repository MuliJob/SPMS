import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token

from allauth.socialaccount.models import SocialAccount

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from backend.serializers.user_serializer import GoogleAuthSerializer, UserSerializer

User = get_user_model()

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Google OAuth authentication"""
        serializer = GoogleAuthSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid access token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        access_token = serializer.validated_data['access_token']

        try:
            # Get user info from Google
            google_response = requests.get(
                f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}',
                timeout=5
            )

            if google_response.status_code != 200:
                return Response(
                    {'error': 'Failed to get user info from Google'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            google_data = google_response.json()

            # Check if user exists
            try:
                user = User.objects.get(email=google_data['email'])

                # Update user info if missing
                if not user.first_name and google_data.get('given_name'):
                    user.first_name = google_data['given_name']
                if not user.last_name and google_data.get('family_name'):
                    user.last_name = google_data['family_name']
                if not user.profile_picture and google_data.get('picture'):
                    user.profile_picture = google_data['picture']
                user.is_email_verified = google_data.get('verified_email', False)
                user.save()

                is_new_user = False

            except User.DoesNotExist:
                # Create new user
                user = User.objects.create_user(
                    username=google_data['email'],
                    email=google_data['email'],
                    first_name=google_data.get('given_name', ''),
                    last_name=google_data.get('family_name', ''),
                    profile_picture=google_data.get('picture', ''),
                    is_email_verified=google_data.get('verified_email', False),
                    role='student'  # Default role
                )

                User.objects.create(user=user)

                is_new_user = True

            # Create or get social account
            social_account, _ = SocialAccount.objects.get_or_create(
                user=user,
                provider='google',
                defaults={
                    'uid': google_data['id'],
                    'extra_data': google_data
                }
            )

            # Generate token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'role': user.role,
                'message': 'Google authentication successful',
                'is_new_user': is_new_user
            })

        except Exception as e:
            return Response(
                {'error': f'Authentication failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

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
