from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import ModelBuilderSerializer, UserSerializer, UcsSystemSerializer
from .models import ModelBuilder, UcsSystem
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.core import serializers
from rest_framework import viewsets, permissions
from .permissions import IsOwner
from api import ucs_manager as ucs
import json
from ucs_manager.connection import ucs_login, ucs_logout
from django.contrib.auth.decorators import login_required

from ucsmsdk.ucshandle import UcsHandle

handle = None

# Create your views here.



class CreateView(generics.ListCreateAPIView):
    """This class defines the create behaviour of our rest api"""
    queryset = UcsSystem.objects.all()
    serializer_class = UcsSystemSerializer
    permission_classes = ( permissions.IsAuthenticated, IsOwner )


    def perform_create(self, serializer):
        """Save the post data when creating a new ml model"""

        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the http GET, PUT and DELETE request for UcsSystem"""
    queryset = UcsSystem.objects.all()
    serializer_class = UcsSystemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)




class UserProfile(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # return Response(serializer.data)

@login_required(login_url='/auth/login/')
@api_view(['GET'])
def getUcsSystems(request):
    if request.method == 'GET':
        print(request.user.username)
        queryset = request.user.ucssystems.filter()              
        # queryset = UcsSystem.objects.all()        
        serializer_class = UcsSystemSerializer(queryset, many=True)        
        # permission_classes = (permissions.IsAuthenticated, IsOwner)
        
        return Response(serializer_class.data)



def getUcsInfo(request):
    try:
        global handle
        global ucs_info
        handle = ucs_login()

        ucs_info = json.dumps(ucs.getUcsInfo(handle), ensure_ascii=False)

        ucs_logout(handle)

    except:
        ucs_logout(handle)
        raise

    return JsonResponse(ucs_info, safe=False)




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


class RackDetails(TemplateView):
    def get(self, request, **kwargs):

        try:
            global handle
            global rackunits
            handle = ucs_login()
            # rackunits = json.dumps(ucs.get_blades(handle), ensure_ascii=False)

            ucs_logout(handle)

        except:
            ucs_logout(handle)
            raise

        return JsonResponse({'test': 'test'}, safe=False)


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
