from rest_framework import permissions

class IsCreator(permissions.BasePermission):
    """
    Limit actions to object creator/admin only.
    """

    def has_permission(self, request, view):
        """
        Check that the user accessing the view is authenticated.
        """

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check that the user accessing the object is:
            - authenticated AND
                - a superuser (admin) or the request method is safe (GET, HEAD or OPTIONS) OR
                - the user who made the request is the creator of the object.
        """

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator.id == request.user.id

class IsSelf(permissions.BasePermission):
    """
    Limit actions to self/admin only.
    """

    def has_permission(self, request, view):
        """
        Check that the user accessing the view is authenticated.
        """

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check that the user accessing the object is:
            - authenticated AND
                - a superuser (admin) or the request method is safe (GET, HEAD or OPTIONS) OR
                - the user who made the request is the object itself.
        """

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class ActionPermission(permissions.BasePermission):
    """
    Map permissions to specific actions (i.e. list, retrieve, create, update, delete).
    Each permission can be listed in a view by using the dictionary variable action_permissions,
    specifying permissions as keys and a list of actions as the values for actions that should
    be enforced by that specific permission.

    For example, the following allows anyone to list and retrieve a resource
    but only the creator to create, update and destroy it:

    Adapted from https://stackoverflow.com/a/47528633.

    action_permissions: {
       AllowAny: ['list', 'retrieve'],
       IsCreator: ['update', 'destroy']
    }
    """

    def has_permission(self, request, view):
        """
        Check view-level permissions against actions specified in 'action_permissions'.
        """

        for cls, actions in getattr(view, 'action_permissions', {}).items():
            if view.action is not None and view.action in actions:
                return cls().has_permission(request, view)
        return False

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permissions against actions specified in 'action_permissions'.
        """

        for cls, actions in getattr(view, 'action_permissions', {}).items():
            if view.action is not None and view.action in actions:
                return cls().has_object_permission(request, view, obj)
        return False
