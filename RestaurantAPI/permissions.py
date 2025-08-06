from rest_framework import permissions

class ReservationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['Manager','AppOwner']).exists():
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        if request.method == "POST":
            return True
        return False


class OrderPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['Manager','AppOwner']).exists():
            return True

        if request.user.groups.filter(name='Deliver_crew').exists():
            if obj.status == 'Preparing':
                if request.method in permissions.SAFE_METHODS:
                    return True

                if request.method in ['PATCH', 'PUT']:
                    return request.data.get('status') == 'Delivered'
            return False

        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user

        if request.method == "POST":
            return True

        return False


class RatingsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name__in=['Manager','AppOwner']).exists():
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
