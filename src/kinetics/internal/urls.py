from django.urls import include, path
from rest_framework import routers

from kinetics.internal.transport.rest.handlers.input_data_handler import get_input_data, create_input_data
from kinetics.internal.transport.rest.handlers.table_parameters_handler import get_table_parameters, create_table_parameters
from kinetics.internal.transport.rest.handlers.solution_data_handler import get_solution

app_name = 'kinetics'

urlpatterns = [
    path('tableparameters/<int:index>/', get_table_parameters),
    path('tableparameters/', create_table_parameters),
    path('solutiondata/<int:index>/', get_solution),
    path('inputdata/<int:index>/', get_input_data),
    path('inputdata/', create_input_data)
]
