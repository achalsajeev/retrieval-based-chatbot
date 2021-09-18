from django.contrib.auth.models import User
from rest_framework import permissions


class IsSuper(permissions.BasePermission):
    """
    Allows access only to "is_admin" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_admin

class IsCompany(permissions.BasePermission):
    """
    Allows access only to "is_company" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_company

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to "is_customer" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_customer

class IsHuman(permissions.BasePermission):
    """
    Allows access only to "is_human_agent" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_human_agent

class IsBotAgent(permissions.BasePermission):
    """
    Allows access only to "is_bot_agent" users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_bot_agent