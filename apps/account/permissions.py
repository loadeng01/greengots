from rest_framework.permissions import BasePermission
#
#
# class IsSuperuserPermission(BasePermission):
#     def has_permission(self, request, view):
#         # Проверяем, является ли пользователь суперпользователем
#         return request.user.is_superuser


class IsActive(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)
