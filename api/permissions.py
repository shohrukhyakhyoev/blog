from rest_framework import permissions


class IsUserItselfOrAdminUser(permissions.BasePermission):    
        """
        Custom permission to check user's authorities who request app users data.
        """
        def has_permission(self, request, view):
             return request.user.is_authenticated
            
        def has_object_permission(self, request, view, obj):
            # Write permissions are only allowed to the owner of the snippet.
            return obj == request.user or request.user.is_staff
        

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only safe methods or admin users to access the view.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
