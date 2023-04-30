from kinetics.internal.models.solution_data import SolutionData
from kinetics.internal.transport.rest.serializers.input_data_serializer import InputDataSerializer
from kinetics.internal.transport.rest.serializers.table_parameters_serializer import TableParametersSerializer


class SolutionDataSerializer:
    def to_dict(self, instance: SolutionData) -> dict:
        input_serializer = InputDataSerializer()
        param_serializer = TableParametersSerializer()

        param_dict = param_serializer.to_dict(instance.input_data.table_parameters)
        input_data = input_serializer.to_dict(instance.input_data)
        input_data["table_parameters"] = param_dict
        return {
            "id": instance.id,
            "input_data": input_data,
            "result": instance.result,
            "experimental_point": instance.experimental_point,
            "error_exp_point": instance.error_exp_point,
            "time": instance.time
        }
