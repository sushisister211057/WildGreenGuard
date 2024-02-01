from django.conf import settings
from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.hashers import check_password
from .models import CustomUserModel


class CustomUserModelBackend(ModelBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.
    """

    def authenticate(self, request, userid=None, display_name=None, **kwargs):
        try:
            user = CustomUserModel.objects.get(userid=userid, display_name=display_name)
        except CustomUserModel.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            return CustomUserModel.objects.get(pk=user_id)
        except CustomUserModel.DoesNotExist:
            return None