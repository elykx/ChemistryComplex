from django.http import JsonResponse
from django.views import View

from kinetics.internal.services.input_data_service import create_input_data, get_input_data_by_id
from kinetics.internal.services.solution_data_service import get_solution_by_id
from kinetics.internal.services.table_parameters_service import create_parameters, get_parameters_by_id
from kinetics.internal.transport.rest.serializers import (
    InputDataSerializer,
    SolutionDataSerializer,
    TableParametersSerializer,
)


class TableParametersView(View):
    def get(self, request, index):
        table_params = get_parameters_by_id(index)
        if table_params:
            serializer = TableParametersSerializer(table_params)
            return JsonResponse(serializer.data, status=200)
        else:
            error = {"error": "TableParameters not found"}
            return JsonResponse(data=error, status=404)

    def post(self, request, *args, **kwargs):
        serializer = TableParametersSerializer(data=request.POST)
        if serializer.is_valid():
            table_param = serializer.save()
            create_parameters(table_param)
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


class SolutionDataView(View):
    def get(self, request, index):
        solution = get_solution_by_id(index)
        if solution:
            serializer = SolutionDataSerializer(solution)
            return JsonResponse(serializer.data, status=200)
        else:
            error = {"error": "SolutionData not found"}
            return JsonResponse(data=error, status=404)


class InputDataView(View):
    def get(self, request, index):
        input_data = get_input_data_by_id(index)
        if input_data:
            serializer = InputDataSerializer(input_data)
            return JsonResponse(serializer.data, status=200)
        else:
            error = {"error": "InputData not found"}
            return JsonResponse(data=error, status=404)

    def post(self, request, *args, **kwargs):
        serializer = InputDataSerializer(data=request.POST)
        if serializer.is_valid():
            input_data = serializer.save()
            create_input_data(input_data)
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)