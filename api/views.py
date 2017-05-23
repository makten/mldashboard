from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import ModelBuilderSerializer, UserSerializer, UcsSystemSerializer, UcsCredentialsSerializer
from .models import ModelBuilder, UcsSystem, UcsCredentials
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
from .ml_operations.modelcreator import ModelOperations as mloperations
from .ml_operations.modelcreator import Predictor as predictor


from ucsmsdk.ucshandle import UcsHandle
from .ml_operations import modelserver
from .ml_operations import settings
import sys
sys.path.append(".")

modelserver.initialize_models(json_path=settings.path_model_json,
                              weights_path=settings.path_model_weight,
                              normalized_x=settings.path_x_normalizer,
                              normalized_y=settings.path_y_normalizer)

handle = None

# def make_password(password, secret_key='2222'):
#     assert password        
#     cipher = AES.new(secret_key, AES.MODE_ECB)
#     encoded = base64.b64encode(cipher.encrypt(password))
#     return encoded


# def unmake_password(encoded_password, secret_key='2222'):
#     assert encoded_password        
#     cipher = cAES.new(secret_key, AES.MODE_ECB)
#     decoded = cipher.decrypt(base64.b64encode(encoded_password))
#     return decoded.strip()


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

    ucs_logout(handle)
    return JsonResponse(ucs_info, safe=False)


@login_required(login_url='/auth/login/')
@api_view(['GET'])
def getUcsCredentials(request):
    if request.method == 'GET':        
        # queryset = request.user.ucssystems.filter()              
        queryset = UcsCredentials.objects.all()        
        serializer_class = UcsCredentialsSerializer(queryset, many=True)        
        # permission_classes = (permissions.IsAuthenticated, IsOwner)
        
        return Response(serializer_class.data)


@login_required(login_url='/auth/login/')
@api_view(['POST'])
def createUcsCredentials(request):
    """ 
        Try connecting to ucs with cred, if success check if item
        exists in db, if not add it else add ucs
    """
    if request.method == 'POST':
        
        serializer = UcsCredentialsSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


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
        ucs_logout(handle)
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
        ucs_logout(handle)
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
        ucs_logout(handle)
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
        ucs_logout(handle)
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
        ucs_logout(handle)
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
        ucs_logout(handle)
        return JsonResponse(faults, safe=False)
