from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import TableParametersSerializer, InputDataSerializer
from .models import TableParameters, InputData

class TableParametersViewSet(viewsets.ModelViewSet):
    queryset = TableParameters.objects.all()
    serializer_class = TableParametersSerializer

class InputDataViewSet(viewsets.ModelViewSet):
    queryset = InputData.objects.all()
    serializer_class = InputDataSerializer