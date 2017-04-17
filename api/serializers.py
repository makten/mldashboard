from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ModelBuilder, UcsSystem, UcsCredentials



class ModelBuilderSerializer(serializers.ModelSerializer):
	""" Serializer to map the Model instance into json format"""
	class Meta:
		"""Meta class to map serializer's fields with the model fields"""
		model = ModelBuilder
		fields = ('id', 'name', 'upload', 'date_created', 'date_modified')
		read_only_fields = ('date_created', 'date_modified')



class UcsSystemSerializer(serializers.ModelSerializer):
	""" Serializer to map the Model instance into json format"""
	owner = serializers.ReadOnlyField(source='owner.username')
	class Meta:
		"""Meta class to map serializer's fields with the model fields"""
		model = UcsSystem
		fields = ('id', 'ipAddress', 'subnet', 'owner', 'date_created', 'date_modified')
		read_only_fields = ('date_created', 'date_modified')



class UcsCredentialsSerializer(serializers.ModelSerializer):
	""" Serializer to map the Model instance into json format"""
	class Meta:
		"""Meta class to map serializer's fields with the model fields"""
		model = UcsCredentials
		fields = ('id', 'cred_username', 'cred_protocol', 'cred_port', 'cred_timeout', 'cred_name', 'date_created', 'date_modified')
		read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
	
	class Meta:
	 	model = User
	 	fields = ('pk', 'username', 'email', 'first_name', 'last_name')
	 		 