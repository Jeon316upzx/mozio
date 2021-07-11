from rest_framework import permissions
from api.models import AccessToken
import datetime
from django.core.exceptions import ValidationError
from api.constants import ACCESS_TOKEN_EXPIRY_TIME


def get_token(request):
    """
    This method is used to get token from request from client
    """
    try:
        token = request.META["HTTP_AUTHORIZATION"].split(' ')[1]
        return AccessToken.objects.get(token=token)

    except (KeyError, IndexError, AccessToken.DoesNotExist, ValidationError):
        return None


class CompanyPermission(permissions.BasePermission):
    """
    Checks if a client ie Company has the right to access a resource
    """

    def has_permission(self, request, view):
        token = get_token(request)
        if token:
            request.user = token.company
            token.expiry += datetime.timedelta(
                minutes=ACCESS_TOKEN_EXPIRY_TIME)
            token.save()
            return True
        else:
            return False
