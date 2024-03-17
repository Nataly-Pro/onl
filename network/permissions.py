from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff and request.user.is_active:
            return True
        else:
            return False
