from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import authenticate
# Create your views here.
from .serializers import UserSerializer, User


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')

        if username and password:

            user = authenticate(request, username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'created': created,
                    'message': 'Login successful',
                }, status=status.HTTP_200_OK)
            else:
                # Return a response for invalid credentials
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)


user_api_view = UserAPIView.as_view()
