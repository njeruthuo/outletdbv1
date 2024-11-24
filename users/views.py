from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from shop.models import Shop
from .models import TextChoices
from .serializers import UserSerializer, User

from django.contrib.auth import authenticate


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data

        username = data.get('email')
        password = data.get('password')

        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        branch_name = data.get('branch_name')

        if username and password:

            user = authenticate(request, username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'created': created,
                    'access':user.access_level,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        elif email and first_name and last_name and branch_name:
            try:
                shop = Shop.objects.get(branch_name=branch_name)
            except Shop.DoesNotExist:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.create(
                email=email, last_name=last_name, first_name=first_name, access_level=TextChoices.EMPLOYEE)

            if user:
                shop.operators.add(user)
                shop.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'User creation unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)


user_api_view = UserAPIView.as_view()
