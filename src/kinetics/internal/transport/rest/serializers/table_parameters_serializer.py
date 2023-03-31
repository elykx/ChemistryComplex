from kinetics.internal.models.table_parameters import TableParameters


class TableParametersSerializer:
    def to_dict(self, instance: TableParameters) -> dict:
        return {
            "id": instance.id,
            "components": instance.components,
            "stages": instance.stages,
            "experiments": instance.experiments
        }

    def to_object(self, data: dict):
        return TableParameters(
            components=data["components"],
            stages=data["stages"],
            experiments=data["experiments"]
        )
