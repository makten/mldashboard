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
from ucs_manager.connection import ucs_login, ucs_logout

from ucsmsdk.ucshandle import UcsHandle

handle = None

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

        try:
            global handle
            global blades
            handle = ucs_login()

            blades = json.dumps(ucs.get_blades(handle), ensure_ascii=False)

            ucs_logout(handle)

        except:
            ucs_logout(handle)
            raise

        return JsonResponse(blades, safe=False)


class ChassisDetails(TemplateView):
    def get(self, request, **kwargs):

        try:
            global handle
            global chassis
            handle = ucs_login()

            chassis = json.dumps(ucs.get_chassis(handle), ensure_ascii=False)

            ucs_logout(handle)

        except:
            ucs_logout(handle)
            raise

        return JsonResponse(chassis, safe=False)

    def getChassisStats(self, request, dn, **kwargs):
        try:
            global handle
            global chassis
            handle = ucs_login()

            faults = json.dumps(
                ucs.getChassisStats(handle, dn), ensure_ascii=False)

            ucs_logout(handle)

        except:
            ucs_logout(handle)
            raise
        return JsonResponse(faults, safe=False)




class ChassisStats(TemplateView):
    def get(self, request, dn, **kwargs):        
        try:
            global handle
            global chassis
            handle = ucs_login()

            faults = json.dumps(
                ucs.getChassisStats(handle, dn), ensure_ascii=False)

            ucs_logout(handle)

        except:
            ucs_logout(handle)
            raise
        return JsonResponse(faults, safe=False)


class BladeFaults(TemplateView):
    def get(self, request, chs, bld, **kwargs):

        try:
            global handle
            global chassis
            handle = ucs_login()

            faults = json.dumps(
                ucs.get_bladefaults(handle, chs, bld), ensure_ascii=False)

            ucs_logout(handle)

        except:
            ucs_logout(handle)
            raise
        return JsonResponse(faults, safe=False)
