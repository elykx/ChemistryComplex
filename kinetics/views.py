import json

import numpy as np
from kinetics.PyDiffeq import ODE_Library
from kinetics.ode_system import System_ODE
from kinetics.utils import to_representation
from rest_framework import generics, viewsets, status
import logging

from rest_framework.response import Response

from .serializers import TableParametersSerializer, InputDataSerializer, SolutionDataSerializer
from .models import TableParameters, InputData, SolutionData

logger = logging.getLogger(__name__)


class TableParametersViewSet(viewsets.ModelViewSet):
    queryset = TableParameters.objects.all()
    serializer_class = TableParametersSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Received POST request with data: %s", request.data)
        return super().create(request, *args, **kwargs)


class InputDataViewSet(viewsets.ModelViewSet):
    queryset = InputData.objects.all()
    serializer_class = InputDataSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input_data = serializer.validated_data

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
            t = np.linspace(initial_time, time, int((time-initial_time)/step) + 1)
            t = [round(x, 6) for x in t]
            system = System_ODE(y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed)
            result = ODE_Library(system, method).solve(t, y0)
            print(result)

            input_data_instance = serializer.save()

            solution_data = SolutionData.objects.create(
                input_data=input_data_instance,
                result=json.dumps(result.tolist()),
                time=json.dumps(t),
            )
            solution_serializer = SolutionDataSerializer(solution_data)
            return Response(solution_serializer.data)
        except Exception as e:
            logger.error("Error creating InputData: %s", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SolutionDataViewSet(viewsets.ModelViewSet):
    queryset = SolutionData.objects.all()
    serializer_class = SolutionDataSerializer

    def get_queryset(self):
        return SolutionData.objects.filter(id=SolutionData.objects.latest('id').id)
