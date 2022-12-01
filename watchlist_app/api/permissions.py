from rest_framework import permissions

# tożsama metoda z kolejną
# class AdminOrReadOnly(permissions.IsAdminUser):
#     def has_permission(self, request, view):
#         # admin_permission = super().has_permission(request, view) obie zmienne oznaczają to samo
#         admin_permission = bool(request.user and request.user.is_staff)
#         return request.method == 'GET' or admin_permission


class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            return bool(request.user and request.user.is_staff)


class ReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            return request.user == obj.author
