from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return bool(obj.user == request.user or request.user.is_staff)
