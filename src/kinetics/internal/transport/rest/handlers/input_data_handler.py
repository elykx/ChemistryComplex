from django.http import JsonResponse
from django.views import View

from kinetics.internal.services.input_data_service import create_input_data, get_input_data_by_id
from kinetics.internal.transport.rest.messages import Message
from kinetics.internal.transport.rest.error import error_response
from kinetics.internal.transport.rest.serializers.input_data_serializer import InputDataSerializer


class InputDataView(View):
    def get(self, request, index):
        input_data = get_input_data_by_id(index)
        if input_data:
            serializer = InputDataSerializer()
            data = serializer.to_dict(input_data)
            response = JsonResponse(data, status=200)
        else:
            error = error_response(Message.INPUT_DATA_NOT_FOUND.value)
            response = JsonResponse(error, status=404)
        return response

    def post(self, request, *args, **kwargs):
        serializer = InputDataSerializer()
        data = request.POST
        input_data = serializer.to_object(data)
        input_d = create_input_data(input_data)
        if input_d:
            data = serializer.to_dict(input_d)
            response = JsonResponse(data, status=201)
        else:
            error = error_response(Message.INPUT_DATA_NOT_CREATED.value)
            response = JsonResponse(error, status=400)
        return response