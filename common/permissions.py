from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="staff").exists()


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="viewer").exists()
