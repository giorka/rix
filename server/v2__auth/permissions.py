from __future__ import annotations

from rest_framework.permissions import BasePermission


class ChangePasswordPermission(BasePermission):
    message = 'Почта не подтверждена.'

    def has_permission(self, request, *args, **kwargs) -> bool:
        return request.user.is_verified
