from rest_framework.permissions import BasePermission


class HasObjectOwnership(BasePermission):
    """
    Checks whether the user has permission on given object
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
