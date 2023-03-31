from kinetics.internal.models.solution_data import SolutionData


def get_solution_by_id(index: int) -> SolutionData:
    solution = SolutionData.objects.filter(input_data__id=index).first()
    return solution
