from rest_framework import permissions as p


class IsAdmin(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class InteractionPermission(p.BasePermission):
    def has_permission(self, request, view):
        if 'view interactions' in request.user.role.permissions:
            return True
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return 'create interactions' in request.user.role.permissions
        return request.user.is_admin


class UserPermission(p.BasePermission):
    def has_permission(self, request, view):
        if 'view users' in request.user.role.permissions:
            return True
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class CustomerPermission(p.BasePermission):
    def has_permission(self, request, view):
        if 'view customers' in request.user.role.permissions:
            return True
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return 'create customers' in request.user.role.permissions
        return request.user.is_admin


class LogsPermission(p.BasePermission):
    def has_permission(self, request, view):
        if 'view logs' in request.user.role.permissions:
            return True
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin