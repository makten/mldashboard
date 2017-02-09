from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ModelBuilder



class ModelBuilderSerializer(serializers.ModelSerializer):
	""" Serializer to map the Model instance into json format"""

	class Meta:
		"""Meta class to map serializer's fields with the model fields"""
		model = ModelBuilder
		fields = ('id', 'name', 'upload', 'date_created', 'date_modified')
		read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
	 	model = User
	 	fields = ('pk', 'username', 'email', 'first_name', 'last_name')
	 		 