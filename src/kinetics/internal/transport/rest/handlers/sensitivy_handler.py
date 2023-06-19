from django.http import JsonResponse

from kinetics.internal.services.sensetivy_service import calculate_sensitivity
from kinetics.internal.services.solution_data_service import get_solution_by_id
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.serializers.sensitivy_serializer import SensitivityResultSerializer


def get_sensitivity(request, index):
    solution = get_solution_by_id(index)
    if solution:
        sensitivity = calculate_sensitivity(solution)
        print(sensitivity.absolute_average)
        serializer = SensitivityResultSerializer()
        data = serializer.to_dict(sensitivity)
        response = JsonResponse(data, status=200)
    else:
        error = error_response(Message.SOLUTION_DATA_NOT_FOUND.value)
        response = JsonResponse(error, status=404)
    return response
