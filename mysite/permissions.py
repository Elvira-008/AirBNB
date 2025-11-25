from  rest_framework import permissions

class CheckCreateBooking(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'guest':
            return True
        return False