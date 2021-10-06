from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user

        return obj.user == current_user or current_user.is_superuser
