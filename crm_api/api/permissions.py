from rest_framework import permissions as p


def check_object_permissions(request, model):
    if request.method == 'POST':
        return request.user.has_perm(f'add_{model}')
    elif request.method == 'DELETE':
        return request.user.has_perm(f'delete_{model}')
    elif request.method == 'PATCH':
        return request.user.has_perm(f'change_{model}')
    return request.user.has_perm(f'view_{model}') or request.user.is_admin


class IsAdmin(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class InteractionPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_interactions')

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'interactions')


class UserPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm('view_users')

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'users')


class CustomerPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm('view_customers')

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'customers')


class EmailLogsPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm('view_emaillogs')

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'emaillog')


class ChatLogsPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm('view_chatlogs')

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'chatlog')
