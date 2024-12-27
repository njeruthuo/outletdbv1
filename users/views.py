from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import TextChoices
from .serializers import UserSerializer, User

from shop.models import Shop
from users.authentication import TokenAuthentication

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
                    'access': user.access_level,
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
            user.set_password('Rapid Rack!')

            if user:
                shop.operators.add(user)
                shop.save()
                return Response({'message': 'User created successfully'}, status=status.HTTP_200_OK)
            return Response({'message': 'User creation unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pass


user_api_view = UserAPIView.as_view()


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def change_password_api_view(request, *args, **kwargs):
    user = request.user

    old_password = request.data.get('oldPassword')
    new_password = request.data.get('newPassword')

    if not old_password or not new_password:
        return Response({'ERROR': 'Both old and new passwords are required.'.upper()}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the old password is correct
    if not user.check_password(old_password):
        return Response({'ERROR': 'Old password is incorrect!'.upper()}, status=status.HTTP_403_FORBIDDEN)

    # Set the new password
    user.set_password(new_password)
    user.save()  # Save the user with the new password

    return Response({'SUCCESS': 'Password was changed successfully!'.upper()}, status=status.HTTP_200_OK)
