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
import sys
sys.path.append(".")
from ucsmsdk.ucshandle import UcsHandle
from .ml_operations import settings

from .ml_operations.model_server import faultPredictor
#from .ml_operations.model_operations import Predictor


# Only testing
import pandas as pd
import numpy as np
from keras.models import load_model, model_from_json
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

try:
    import cPickle as pickle
except:
    import pickle


predictor = None
handle = None

def getModel(model_path):
        
    return load_model(model_path)


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


def getPowerStats(request):
    try:
        global handle
        global ucs_powerstat
        handle = ucs_login()

        ucs_powerstat = json.dumps(ucs.getEquipmentPsuInputStats(handle), ensure_ascii=False)

        ucs_logout(handle)

    except:
        ucs_logout(handle)
        raise

    ucs_logout(handle)

    return JsonResponse(ucs_powerstat, safe=False)



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
    
    

def getPredictions(request):      
    
    # try:
    
    #     from random import randint
        
    #     dataframe = pd.read_csv("./api/ml_operations/pickles/random_cutout_test.csv")
    #     dataset = dataframe.values
        
    #     X = dataset[:randint(1, len(dataset)),0:200].astype(float)
        
    #     model = getModel(settings.model_path)
    #     x_normed = normalize_input(X, settings.path_x_normalizer)
            
    #     y_pred = model.predict_classes(x_normed)
        
    #     predictions = json.dumps(list(denormalize_prediction(y_pred, settings.path_y_normalizer)))
               
        
    # except:
        
    #     return Exception('Something went wrong')
    
    # from keras.backend.tensorflow_backend import clear_session
    
    # clear_session()    
    predictions = faultPredictor()
        
    return JsonResponse(predictions, safe=False )









