from django.urls import path

from kinetics.internal.transport.rest.handlers.input_data_handler import create_input_data, get_input_data
from kinetics.internal.transport.rest.handlers.solution_data_handler import get_solution, save_solution_report
from kinetics.internal.transport.rest.handlers.table_parameters_handler import (
    create_table_parameters,
    get_table_parameters,
)

app_name = 'kinetics'

urlpatterns = [
    path('tableparameters/<int:index>/', get_table_parameters),
    path('tableparameters/', create_table_parameters),
    path('solutiondata/<int:index>/', get_solution),
    path('solutiondata/save/<int:index>/', save_solution_report),
    path('inputdata/<int:index>/', get_input_data),
    path('inputdata/', create_input_data)
]
