from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Only allow admins to make changes."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated() and \
            request.user.is_staff
