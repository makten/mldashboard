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
from api import ucs_manager as ucs
import json

from ucsmsdk.ucshandle import UcsHandle

# Connection
handle = UcsHandle("192.168.202.147", "ucspe", "ucspe")

#Login
handle.login()


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



class BladeDetails(TemplateView):

	def get(self, request, **kwargs):

		context = {
			'data': [
				{
                    'name': 'Celeb 1',
                    'worth': '3567892'
                },
                {
                    'name': 'Celeb 2',
                    'worth': '23000000'
                },
                {
                    'name': 'Celeb 3',
                    'worth': '1000007'
                },
                {
                    'name': 'Celeb 4',
                    'worth': '456789'
                }
			]
		}

		blades = json.dumps(ucs.get_blades(handle), ensure_ascii=False)
		

		# blades = ucs.domain_serials(handle)

		# x = json.dumps(blades)
		

		return JsonResponse(blades, safe=False)

# class BladeDetails(generics.RetrieveAPIView):
    	
# 		def get():
    			
# 				return JsonResponse({'hello': 'world'})
		
		
		