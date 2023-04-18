from django.http import JsonResponse

from kinetics.internal.services.excel_service import create_excel_solution
from kinetics.internal.services.solution_data_service import get_solution_by_id
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.serializers.solution_data_serializer import SolutionDataSerializer


def get_solution(request, index):
    solution = get_solution_by_id(index)
    if solution:
        serializer = SolutionDataSerializer()
        data = serializer.to_dict(solution)
        response = JsonResponse(data, status=200)
    else:
        error = error_response(Message.SOLUTION_DATA_NOT_FOUND.value)
        response = JsonResponse(error, status=404)
    return response


def save_solution_report(request, index):
    solution = get_solution_by_id(index)
    if solution:
        create_excel_solution(solution)
        error = error_response(Message.SOLUTION_DATA_NOT_FOUND.value)
        response = JsonResponse(data=error, status=200)
    else:
        error = error_response(Message.SOLUTION_DATA_NOT_FOUND.value)
        response = JsonResponse(error, status=404)
    return response
