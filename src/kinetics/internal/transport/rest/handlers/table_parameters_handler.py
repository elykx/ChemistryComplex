from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token

from kinetics.internal.services.table_parameters_service import create_parameters, get_parameters_by_id
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.serializers.table_parameters_serializer import TableParametersSerializer


class TableParametersView(View):
    def get(self, request, index):
        table_params = get_parameters_by_id(index)
        if table_params:
            serializer = TableParametersSerializer()
            data = serializer.to_dict(table_params)
            response = JsonResponse(data, status=200)
        else:
            error = error_response(Message.TABLE_PARAMETERS_NOT_FOUND.value)
            response = JsonResponse(error, status=404)
        return response

    def post(self, request, *args, **kwargs):
        serializer = TableParametersSerializer()
        data = request.POST
        table_param = serializer.to_object(data)
        param = create_parameters(table_param)
        if param:
            data = serializer.to_dict(param)
            response = JsonResponse(data, status=201)
        else:
            error = error_response(Message.TABLE_PARAMETERS_NOT_CREATED.value)
            response = JsonResponse(error, status=400)
        return response
