from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from kinetics.views import TableParametersViewSet, InputDataViewSet, SolutionDataViewSet

app_name='kinetics'
router = routers.DefaultRouter()
router.register(r'tableparameters', TableParametersViewSet)
router.register(r'inputdata', InputDataViewSet)
router.register(r'solutiondata', SolutionDataViewSet)
urlpatterns = [
    path('', include(router.urls)),

]