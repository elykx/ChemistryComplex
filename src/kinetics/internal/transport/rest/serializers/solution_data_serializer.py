from kinetics.internal.models.solution_data import SolutionData


class SolutionDataSerializer:
    def to_dict(self, instance: SolutionData) -> dict:
        return {
            "id": instance.id,
            "input_data": instance.input_data,
            "result": instance.result,
            "experimental_point": instance.experimental_point,
            "time": instance.time
        }
