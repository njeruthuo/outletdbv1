from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from .models import User


class EmailAuthenticationBackend(BaseBackend):
    """
    Custom authentication backend that allows login using either email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find the user by either username or email
            user = User.objects.get(
                Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            # If no user exists with the provided credentials, return None
            return None

        # Check the password
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
