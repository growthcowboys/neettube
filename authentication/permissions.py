from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsUnauthenticatedOrStaffOrNoPost(BasePermission):


    def has_permission(self, request, view):

        if request.user.is_authenticated and not request.user.is_staff:

            return request.method != "POST"

        return True
    

class IsStaffOrUserOrSafeMethods(BasePermission):


    def has_object_permission(self, request, view, user):
        
        if request.user.is_staff:

            return True
        
        return request.user == user or request.method in SAFE_METHODS