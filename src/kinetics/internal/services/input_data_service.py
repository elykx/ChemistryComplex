from kinetics.internal.models.input_data import InputData


def get_input_data_by_id(index: int) -> InputData:
    input_data = InputData.objects.filter(id=index).first()
    return input_data


def create_input_data(input: InputData) -> InputData:
    input_data = InputData.objects.create()
    return input_data