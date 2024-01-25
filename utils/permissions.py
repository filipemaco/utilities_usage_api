from rest_framework import permissions


class IsLoggedInAndOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


# I had to rewrite IsAdminUser, django rest framework has a bug:
# https://github.com/encode/django-rest-framework/issues/7117
class IsAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
