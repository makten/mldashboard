from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import ModelBuilderSerializer, UserSerializer
from .models import ModelBuilder
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.core import serializers
from rest_framework import viewsets


# Create your views here.

class CreateView(generics.ListCreateAPIView):
	"""This class defines the create behaviour of our rest api"""
	queryset = ModelBuilder.objects.all()
	serializer_class = ModelBuilderSerializer

	def perform_create(self, serializer):
		"""Save the post data when creating a new ml model"""
		serializer.save()



class DetailsView(generics.RetrieveUpdateDestroyAPIView):
	"""Handles the http GET, PUT and DELETE request for MODELBUILDER"""
	queryset = ModelBuilder.objects.all()
	serializer_class = ModelBuilderSerializer


class UserProfile(generics.ListCreateAPIView):			
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):

	queryset = User.objects.all()	
	serializer_class = UserSerializer	
	# return Response(serializer.data)
		
		
		