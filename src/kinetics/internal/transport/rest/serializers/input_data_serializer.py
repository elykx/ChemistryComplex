from kinetics.internal.models.input_data import InputData
from kinetics.internal.transport.rest.serializers.table_parameters_serializer import TableParametersSerializer


class InputDataSerializer:
    def to_dict(self, instance: InputData) -> dict:
        param_serializer = TableParametersSerializer()
        param_dict = param_serializer.to_dict(instance.table_parameters)
        return {
            "id": instance.id,
            "table_parameters": param_dict,
            "initial_time": instance.initial_time,
            "time": instance.time,
            "step": instance.step,
            "matrix_stechiometric_coefficients": instance.matrix_stechiometric_coefficients,
            "matrix_indicators": instance.matrix_indicators,
            "experimental_data": instance.experimental_data,
            "constants_speed": instance.constants_speed,
            "method": instance.method
        }

    def to_object(self, data: dict):
        return InputData(
            table_parameters=data["table_parameters"],
            initial_time=data["initial_time"],
            time=data["time"],
            step=data["step"],
            matrix_stechiometric_coefficients=data["matrix_stechiometric_coefficients"],
            matrix_indicators=data["matrix_indicators"],
            experimental_data=data["experimental_data"],
            constants_speed=data["constants_speed"],
            method=data["method"]
        )
