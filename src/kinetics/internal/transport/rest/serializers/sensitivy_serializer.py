from kinetics.internal.models.sensitivy_result import SensitivityResult


class SensitivityResultSerializer:
    def to_dict(self, instance: SensitivityResult) -> dict:
        return {
            "id": instance.id,
            "average": instance.average,
            "absolute_average": instance.absolute_average,
            "standart_deviation": instance.standart_deviation,
            "constant_speed_num": instance.constant_speed_num,
            "time": instance.time,
        }
