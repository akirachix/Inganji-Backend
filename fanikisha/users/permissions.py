from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Custom permission to only allow admin users to access the view."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'admin'

class IsSacco(permissions.BasePermission):
    """Custom permission to only allow SACCO users to access the view."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'sacco'

class IsCooperative(permissions.BasePermission):
    """Custom permission to only allow cooperative users to access the view."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'cooperative'
