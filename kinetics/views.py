import json

import numpy as np
from kinetics.solution_services.changer_exp_data import change_exp_data
from kinetics.solution_services.ode_system import System_ODE
from kinetics.utils import to_representation
from pydiffeq import ODE_Library
from rest_framework import viewsets, status
import logging

from rest_framework.response import Response

from .serializers import TableParametersSerializer, InputDataSerializer, SolutionDataSerializer
from .models import TableParameters, InputData, SolutionData

logger = logging.getLogger(__name__)


class TableParametersViewSet(viewsets.ModelViewSet):
    queryset = TableParameters.objects.all()
    serializer_class = TableParametersSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info("Received POST request with data: %s", request.data)
        return super().create(request, *args, **kwargs)


class InputDataViewSet(viewsets.ModelViewSet):
    queryset = InputData.objects.all()
    serializer_class = InputDataSerializer

    def create(self, request, *args, **kwargs):
        table_param_id = request.data.get("table_parameters")
        table_param = TableParameters.objects.get(id=table_param_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_data = serializer.validated_data
        input_data['table_parameters'] = table_param

        matrix_stechiometric_coefficients = to_representation(input_data.get('matrix_stechiometric_coefficients'))
        matrix_indicators = to_representation(input_data.get('matrix_indicators'))
        experimental_data = to_representation(input_data.get('experimental_data'))
        constants_speed = to_representation(input_data.get('constants_speed'))
        initial_time = input_data['initial_time']
        time = input_data['time']
        step = input_data['step']
        method = input_data['method']
        try:
            logger.info("Solving System ODE %s", request.data)
            y0 = experimental_data[0][1:]
            t = np.linspace(initial_time, time, int((time - initial_time) / step) + 1)
            t = [round(x, 6) for x in t]
            system = System_ODE(y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed)
            result = ODE_Library(system, method).solve(t, y0)
            experimental_point = change_exp_data(experimental_data, result, t)
            print(y0)
            input_data_instance = serializer.save()
            solution_data = SolutionData.objects.create(
                input_data=input_data_instance,
                result=json.dumps(result.tolist()),
                time=json.dumps(t),
                experimental_point=json.dumps(experimental_point),
            )
            solution_serializer = SolutionDataSerializer(solution_data)
            return Response(solution_serializer.data)
        except Exception as e:
            logger.error("Error creating InputData: %s", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SolutionDataViewSet(viewsets.ModelViewSet):
    queryset = SolutionData.objects.all()
    serializer_class = SolutionDataSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return SolutionData.objects.get(input_data__id=pk)
        except SolutionData.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


