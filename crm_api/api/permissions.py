from rest_framework import permissions as p


def check_object_permissions(request, model, app_name=None):
    if request.method == 'POST':
        return request.user.has_perm(f'{app_name}.add_{model}')
    if request.method == 'DELETE':
        return request.user.has_perm(f'{app_name}.delete_{model}')
    if request.method == 'PATCH':
        return request.user.has_perm(f'{app_name}.change_{model}')
    return request.user.has_perm(
        f'{app_name}.view_{model}'
    ) or request.user.is_admin


class IsAdmin(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class InteractionPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('interactions.view_interaction')

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'interaction', 'interactions')


class UserPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm(
            'users.view_user'
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'user')


class CustomerPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm(
            'customers.view_customer'
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'customer')


class EmailLogsPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm(
            'interactions.view_emaillog'
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'emaillog')


class ChatLogsPermission(p.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.has_perm(
            'interactions.view_chatlog'
        )

    def has_object_permission(self, request, view, obj):
        return check_object_permissions(request, 'chatlog')
