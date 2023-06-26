from rest_framework import permissions as p


class IsAdmin(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class InteractionPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_interactions')

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.has_perm('create_interactions')
        return request.user.has_perm('view_interactions')


class UserPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm('view_users')

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or request.user.has_perm('create_users')


class CustomerPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm('view_customers')

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.has_perm('create_customers')
        return request.user.is_admin


class LogsPermission(p.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.has_perm('create_logs')
        elif request.method == 'GET':
            return request.user.has_perm('view_logs')
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('view_logs')
