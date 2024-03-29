import copy
import time
import numpy as np
from pydiffeq import ODE_Library

from kinetics.internal.models.input_data import InputData
from kinetics.internal.services.ode_system import System_ODE
from kinetics.internal.services.solution_data_service import create_solution
from kinetics.internal.services.utils import to_representation


def get_input_data_by_id(index: int) -> InputData:
    input_data = InputData.objects.filter(id=index).first()
    return input_data


def create_input(input_d: InputData) -> InputData:
    input_data = InputData.objects.create(
        table_parameters=input_d.table_parameters,
        initial_time=input_d.initial_time,
        time=input_d.time,
        step=input_d.step,
        matrix_stechiometric_coefficients=input_d.matrix_stechiometric_coefficients,
        matrix_indicators=input_d.matrix_indicators,
        experimental_data=input_d.experimental_data,
        constants_speed=input_d.constants_speed,
        method=input_d.method
    )
    return input_data


def matrix_to_representation(data):
    data = data.replace('"', "").replace('"', "")
    rows = data.split('],[')
    rows = [row.replace('[', '').replace(']', '') for row in rows]
    return [list(map(float, row.split(','))) for row in rows]


def change_exp_data(experimental_data, solution, time):
    exp_point = experimental_data
    if len(time) != len(solution):
        return experimental_data
    for i in range(len(time)):
        for j in range(len(experimental_data)):
            if experimental_data[j][0] == time[i]:
                exp_point[j][1:] = solution[i]
    return exp_point


def calculate_error(experimental_data, calculated_data):
    error_point = experimental_data
    for i in range(len(experimental_data)):
        for j in range(1, len(experimental_data[i])):
            if experimental_data[i][j] == 0:
                error_point[i][j] = 0
            else:
                error_point[i][j] = np.round(((abs(experimental_data[i][j] - calculated_data[i][j])) / experimental_data[i][j]) * 100, 5)
    return error_point


def solve_ode(input_data: InputData):
    matrix_stechiometric_coefficients = to_representation(input_data.matrix_stechiometric_coefficients)
    matrix_indicators = to_representation(input_data.matrix_indicators)
    experimental_data = to_representation(input_data.experimental_data)
    constants_speed = to_representation(input_data.constants_speed)
    initial_time = input_data.initial_time
    t = input_data.time
    step = input_data.step
    method = input_data.method

    y0 = experimental_data[0][1:]
    t = np.linspace(initial_time, t, int((t - initial_time) / step) + 1)
    t = [round(x, 6) for x in t]

    system = System_ODE(y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed)
    lib = ODE_Library(system, method)
    start_time = time.time()
    result, t_eval = lib.solve(t, y0)
    runtime = round(time.time() - start_time, 5)
    result = np.round(result, 3)
    t_eval = np.round(t_eval, 2)
    experimental_point = change_exp_data(copy.deepcopy(experimental_data), result, t)
    error_exp_point = calculate_error(copy.deepcopy(experimental_data), copy.deepcopy(experimental_point))
    solution = create_solution(input_data, result, t_eval, experimental_point, error_exp_point, runtime)
    return solution
