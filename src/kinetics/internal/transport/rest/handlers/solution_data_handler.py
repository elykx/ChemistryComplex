from django.http import JsonResponse, HttpResponse

from kinetics.internal.services.excel_service import create_excel_solution
from kinetics.internal.services.sensetivy_service import calculate_sensitivity
from kinetics.internal.services.solution_data_service import get_solution_by_id
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.serializers.solution_data_serializer import SolutionDataSerializer


def get_solution(request, index):
    solution = get_solution_by_id(index)
    if solution:
        # sens = calculate_sensitivity(solution)
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
        excel_file, file_name = create_excel_solution(solution)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        response.write(excel_file.read())
    else:
        error = error_response(Message.SOLUTION_DATA_NOT_FOUND.value)
        response = JsonResponse(error, status=404)
    return response
