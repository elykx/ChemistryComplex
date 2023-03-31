from django.urls import include, path
from rest_framework import routers

from kinetics.internal.transport.rest.handlers import SolutionDataView, TableParametersView
from kinetics.internal.transport.rest.views import InputDataViewSet, SolutionDataViewSet

app_name='kinetics'
router = routers.DefaultRouter()
router.register(r'inputdata', InputDataViewSet)
router.register(r'solutiondata', SolutionDataViewSet)

urlpatterns = [
    path('tableparameters/<int:index>', TableParametersView.as_view()),
    path('solution/<int:index>', SolutionDataView.as_view()),
    path('', include(router.urls)),
]