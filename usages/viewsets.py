from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas.openapi import AutoSchema

from utils.permissions import IsLoggedInAndOwner, IsAdminUser

from .models import Usage, UsageType
from .serializers import (UsageSerializer, UsageTypeSerializer,
                          UsageCreateUpdateSerializer)


class UsageViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(
        tags=['Usage']
    )
    serializers = {
        'default': UsageSerializer,
        'list': UsageSerializer,
        'create': UsageCreateUpdateSerializer,
        'update': UsageCreateUpdateSerializer,
        'partial_update': UsageCreateUpdateSerializer,
    }
    queryset = Usage.objects.all()
    permission_classes = [IsLoggedInAndOwner | IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'usage_at': ['gte', 'lte'],
        'usage_type__name': ['exact', 'icontains'],
        'amount': ['gte', 'lte'],
        'calculated_emissions': ['gte', 'lte'],
    }
    ordering = ['-usage_at']
    ordering_fields = [
        'usage_at', 'amount', 'calculated_emissions', 'usage_type__name']

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def get_queryset(self):
        if self.action != 'list' or self.request.user.is_staff:
            return self.queryset

        return self.queryset.filter(user=self.request.user)


class UsageTypeViewSet(viewsets.ModelViewSet):
    schema = AutoSchema(
        tags=['Usage Type']
    )
    queryset = UsageType.objects.all()
    serializer_class = UsageTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'unit': ['exact'],
        'factor': ['exact', 'gte', 'lte']
    }
    ordering_fields = '__all__'

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
