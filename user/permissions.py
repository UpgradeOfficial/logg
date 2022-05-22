from rest_framework.permissions import BasePermission
from user.models import User


class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.USER_TYPE.STUDENT == User.USER_TYPE.STUDENT)

class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.USER_TYPE.STAFF == User.USER_TYPE.STAFF)

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.USER_TYPE.TEACHER == User.USER_TYPE.TEACHER)

class SchoolPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.USER_TYPE.SCHOOL == User.USER_TYPE.SCHOOL)

class AdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.USER_TYPE.ADMINISTRATOR == User.USER_TYPE.ADMINISTRATOR)

class GuardianPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.USER_TYPE.GUARDIAN == User.USER_TYPE.GUARDIAN)