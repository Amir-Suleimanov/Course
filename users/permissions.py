from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    message = 'У вас нет прав чтобы изменять этот объект'

    def has_permission(self, request, view):
        
        if request.method == 'DELETE':
            return request.user.is_staff
        
        if request.method in SAFE_METHODS:
            return True
        
        return True


class IsUserOrAdmin(BasePermission):
    message = 'У вас нет прав чтобы просматривать эту страницу'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj == request.user