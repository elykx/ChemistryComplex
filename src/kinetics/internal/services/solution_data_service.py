import json

from kinetics.internal.models.input_data import InputData
from kinetics.internal.models.solution_data import SolutionData


def get_solution_by_id(index: int) -> SolutionData:
    solution = SolutionData.objects.filter(input_data__id=index).first()
    return solution


def create_solution(input_data: InputData, result, t_eval, exp_point, error_exp_point, runtime) -> SolutionData:
    solution_data = SolutionData.objects.create(
        input_data=input_data,
        result=json.dumps(result.tolist()),
        time=json.dumps(t_eval.tolist()),
        experimental_point=json.dumps(exp_point),
        error_exp_point=json.dumps(error_exp_point),
        runtime=runtime,
    )
    return solution_data
