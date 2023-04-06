import numpy as np
from pydiffeq import ODE_Library

from kinetics.internal.models.input_data import InputData
from kinetics.internal.services.solution_data_service import create_solution
from kinetics.internal.services.solution_services.changer_exp_data import change_exp_data
from kinetics.internal.services.solution_services.ode_system import System_ODE
from kinetics.utils import to_representation


def get_input_data_by_id(index: int) -> InputData:
    input_data = InputData.objects.filter(id=index).first()
    return input_data


def create_input_data(input_d: InputData) -> InputData:
    input_data = InputData.objects.create()
    return input_data


def matrix_to_representation(data):
    data = data.replace('"', "").replace('"', "")
    rows = data.split('],[')
    rows = [row.replace('[', '').replace(']', '') for row in rows]
    return [list(map(float, row.split(','))) for row in rows]


def solve_ode(input_data):
    matrix_stechiometric_coefficients = to_representation(input_data.get('matrix_stechiometric_coefficients'))
    matrix_indicators = to_representation(input_data.get('matrix_indicators'))
    experimental_data = to_representation(input_data.get('experimental_data'))
    constants_speed = to_representation(input_data.get('constants_speed'))
    initial_time = input_data['initial_time']
    time = input_data['time']
    step = input_data['step']
    method = input_data['method']

    y0 = experimental_data[0][1:]
    t = np.linspace(initial_time, time, int((time - initial_time) / step) + 1)
    t = [round(x, 6) for x in t]
    system = System_ODE(y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed)
    result, t_eval = ODE_Library(system, method).solve(t, y0)
    experimental_point = change_exp_data(experimental_data, result, t)
    solution = create_solution(input_data, result, t_eval, experimental_point)

    return solution
