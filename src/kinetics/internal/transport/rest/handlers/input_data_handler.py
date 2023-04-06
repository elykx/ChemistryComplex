import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from kinetics.internal.services.input_data_service import create_input, get_input_data_by_id, solve_ode
from kinetics.internal.services.table_parameters_service import get_parameters_by_id
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.serializers.input_data_serializer import InputDataSerializer
from kinetics.internal.transport.rest.serializers.solution_data_serializer import SolutionDataSerializer


def get_input_data(request, index):
    input_data = get_input_data_by_id(index)
    if input_data:
        serializer = InputDataSerializer()
        data = serializer.to_dict(input_data)
        response = JsonResponse(data, status=200)
    else:
        error = error_response(Message.INPUT_DATA_NOT_FOUND.value)
        response = JsonResponse(error, status=404)
    return response


@csrf_exempt
def create_input_data(request, *args, **kwargs):
    serializer = InputDataSerializer()
    data = json.loads(request.body)
    table_param_id = data["table_parameters"]
    table_param = get_parameters_by_id(table_param_id)
    data['table_parameters'] = table_param
    input_data = serializer.to_object(data)

    current_data = create_input(input_data)
    solution = solve_ode(current_data)
    if solution:
        solution_serializer = SolutionDataSerializer()
        data = solution_serializer.to_dict(solution)
        print(data)
        response = JsonResponse(data, status=201)
    else:
        error = error_response(Message.INPUT_DATA_NOT_CREATED.value)
        response = JsonResponse(error, status=400)
    return response


