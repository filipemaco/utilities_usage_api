from django.contrib.auth import get_user_model

from rest_framework.schemas.openapi import AutoSchema
from rest_framework import viewsets

from utils.permissions import IsOwnUser, IsAdminUser

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(
        tags=['Users']
    )
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'put', 'delete', 'head']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwnUser | IsAdminUser]
        return [permission() for permission in permission_classes]
