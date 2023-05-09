import numpy as np
from pydiffeq import ODE_Library

from kinetics.internal.models.sensitivy_result import SensitivityResult
from kinetics.internal.models.solution_data import SolutionData
from kinetics.internal.services.method_morris.method_morris import morris_sample, scale_sample, get_delta, \
    elementary_effects
from kinetics.internal.services.ode_system import System_ODE
from kinetics.internal.services.utils import to_representation


def calculate_sensitivity(solution: SolutionData) -> SensitivityResult:
    num_trajectory = 100
    grid_level = 4

    matrix_stechiometric_coefficients = to_representation(solution.input_data.matrix_stechiometric_coefficients)
    matrix_indicators = to_representation(solution.input_data.matrix_indicators)
    experimental_data = to_representation(solution.input_data.experimental_data)
    constants_speed = to_representation(solution.input_data.constants_speed)
    initial_time = solution.input_data.initial_time
    time = solution.input_data.time
    step = solution.input_data.step
    method = solution.input_data.method
    y0 = experimental_data[0][1:]

    t = np.linspace(initial_time, time, int((time - initial_time) / step) + 1)
    t = [round(x, 6) for x in t]

    system = System_ODE(y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed)
    lib = ODE_Library(system, method)
    result, t_eval = lib.solve(t, y0)
    result = np.round(result, 3)
    cs = []
    for i in range(len(constants_speed)):
        cs.append(constants_speed[i][0])

    b = morris_sample(len(cs), num_trajectory, grid_level)
    scaled_sample = scale_sample(b, cs, 0.25)

    delta = get_delta(grid_level)
    mu, mu_star, sigma, num_const = elementary_effects(scaled_sample, solution, delta)
    mu = np.round(mu, 3)
    mu_star = np.round(mu_star, 3)
    sigma = np.round(sigma, 3)

    sensitivity = SensitivityResult.objects.create(
        average=mu,
        absolute_average=mu_star,
        standart_deviation=sigma,
        constant_speed_num=num_const,
    )
    return sensitivity
