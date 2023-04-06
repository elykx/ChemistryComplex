from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from kinetics.internal.services.table_parameters_service import create_parameters, get_parameters_by_id
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.serializers.table_parameters_serializer import TableParametersSerializer


class TableParametersView(View):
    @csrf_exempt
    def get(self, request, index):
        table_params = get_parameters_by_id(index)
        if table_params:
            serializer = TableParametersSerializer()
            data = serializer.to_dict(table_params)
            response = JsonResponse(data, status=200)
            response['X-CSRFToken'] = get_token(request)
        else:
            error = error_response(Message.TABLE_PARAMETERS_NOT_FOUND.value)
            response = JsonResponse(error, status=404)
            response['X-CSRFToken'] = get_token(request)
        return response

    @csrf_exempt
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
