# -*- coding: utf-8 -*-
from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Define si se tiene permiso para realizar la acción
        :param request: objeto request
        :param view: vista desde donde se ejecuta la acción
        :return: boolean
        """
        from api import UserDetailAPI # evita la interdependencia con api.py

        if request.method == "POST":
            return True

        # si es superuser, puede hacer un GET, PUT y DELETE si quiere
        elif request.user.is_superuser:
            return True

        # si no es superuser, le dejamos acceder sólo al detalle
        elif isinstance(view, UserDetailAPI):
            return True

        # en cualquier otro caso, no permitimos realizar la acción
        else:
            return False


    def has_object_permission(self, request, view, obj):
        """
        Define si se tiene permiso para hacer PUT o DELETE
        sobre obj.
        Sólo tiene permiso si es propietario o es superuser
        :param request: objeto request
        :param view: vista desde donde se ejecuta
        :param obj: objeto sobre el que se ejecuta
        :return: boolean
        """
        if request.user.is_superuser or obj.owner == request.user:
            return True
        else:
            return False




























