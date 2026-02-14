from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    """بررسی دسترسی کاربر بر اساس نقش"""

    def __init__(self, permission_slug):
        self.permission_slug = permission_slug

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_permission(self.permission_slug)
