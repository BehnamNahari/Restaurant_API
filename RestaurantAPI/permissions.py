from rest_framework import permissions

class IsOwnerOrStaffCanEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff

class IsOwnerOrStaffReadOnlyDeleteDenied(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE']:
            return request.user.is_staff

        if request.method in permissions.SAFE_METHODS or request.method in ['PUT','PATCH']:
            return obj.user == request.user or request.user.is_staff

        return False