from rest_framework.permissions import BasePermission
from .models import UcsSystem


class IsOwner(BasePermission):
	"""Custom permission class to allow only ucssystem owners to edit"""
	def has_object_permission(self, request, view, obj):
		""" Return True if permission is granted to the ucssystem onwer"""
		if isinstance(obj, UcsSystem):
			return obj.owner == request.user
		return obj.owner == request.user
		