from django.urls import include, path
from rest_framework import routers

from kinetics.internal.transport.rest.handlers.input_data_handler import InputDataView
from kinetics.internal.transport.rest.handlers.table_parameters_handler import TableParametersView
from kinetics.internal.transport.rest.handlers.solution_data_handler import SolutionDataView

app_name='kinetics'
# router = routers.DefaultRouter()
# router.register(r'inputdata', InputDataViewSet)
# router.register(r'solutiondata', SolutionDataViewSet)

urlpatterns = [
    path('tableparameters/<int:index>', TableParametersView.as_view()),
    path('solution/<int:index>', SolutionDataView.as_view()),
    path('inputdata/<int:index>', InputDataView.as_view())
    # path('', include(router.urls)),
]