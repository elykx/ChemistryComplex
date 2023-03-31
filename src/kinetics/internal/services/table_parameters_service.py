from kinetics.internal.models.table_parameters import TableParameters


def get_parameters_by_id(index: int) -> TableParameters:
    parameters = TableParameters.objects.filter(id=index).first()
    return parameters


def create_parameters(param: TableParameters) -> TableParameters:
    parameters = TableParameters.objects.create(
        components=param.components,
        stages=param.stages,
        experiments=param.experiments)
    return parameters
