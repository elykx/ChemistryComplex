import numpy as np
import math
import copy

from pydiffeq import ODE_Library

from kinetics.internal.services.ode_system import System_ODE
from kinetics.internal.services.utils import to_representation


def get_delta(num_levels):
    delta = num_levels / (2 * (num_levels - 1))
    return delta


def get_x_star(num_levels, num_input, delta):
    grid = np.linspace(0, 1 - delta, int(num_levels / 2))
    x_star = np.random.choice(grid, size=num_input)
    return x_star


def compute_Bstar(num_input, delta, x_star):
    k = num_input

    B = np.tril(np.ones((k + 1, k)), -1)  # Obtain strictly lower triangular matrix

    # Obtain matrices J
    J_copy = np.ones((k + 1, 1))
    J = np.ones((k + 1, k))

    # Obtain matrix D*
    D_star = np.diag(np.random.choice([-1, 1], size=k))

    # Obtain permutation matrix P*
    P_star = np.eye(k, k)
    P_star = np.random.permutation(P_star)

    # Computation of B* is divided into three parts
    part_a = ((np.matmul(2 * B - J, D_star) + J) * delta / 2)
    part_b = part_a + J_copy * x_star
    B_star = np.matmul(part_b, P_star)
    return B_star


def morris_sample(num_input, n_trajectories, num_levels):
    k = num_input

    delta = get_delta(num_levels)

    morris_sample = np.zeros([n_trajectories, k + 1, k])

    for i in range(n_trajectories):
        x_star = get_x_star(num_levels, k, delta)

        morris_sample[i, :, :] = compute_Bstar(k, delta, x_star)

    return morris_sample


def elementary_effects(sample, solution, delta, num_trajectory):
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

    s = sample.tolist()
    y = sample.tolist()
    for i in range(len(s)):
        for j in range(len(s[i])):
            for k in range(len(constants_speed)):
                constants_speed[k][0] = s[i][j][k]
            system = System_ODE(y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed)
            lib = ODE_Library(system, method)
            y[i][j], t_eval = lib.solve(t, y0)

    numberofconst = []

    for i in range(len(sample)):
        for j in range(1, len(sample[i])):
            for k in range(len(sample[i][j])):
                if sample[i][j][k] != sample[i][j-1][k]:
                    numberofconst.append(k+1)

    n_args = []

    for i in range(len(constants_speed)):
       n_args.append(i+1)

    ee1 = [[0 for x in range(len(constants_speed))] for y in range(len(t_eval))]
    ee2 = [[0 for x in range(len(constants_speed))] for y in range(len(t_eval))]

    for i in range(len(s)):
        for j in range(len(s[i])):
            for k in range(len(n_args)):
                for tt in range(len(t_eval)):
                    y1 = 0
                    y2 = 0
                    for l in range(len(y[0][0][0])):
                        y1 += y[i][j - 1][tt][l]
                        y2 += y[i][j][tt][l]
                    if s[i][j][k] > s[i][j - 1][k]:
                        e = (y2-y1) / delta
                    else:
                        e = (y1-y2) / delta
                    ee1[tt][k] += e
                    ee2[tt][k] += math.fabs(e)


    ee_mean = [[0 for x in range(len(constants_speed))] for y in range(len(t_eval))]
    ee_absmean = [[0 for x in range(len(constants_speed))] for y in range(len(t_eval))]
    ee_std = [[0 for x in range(len(constants_speed))] for y in range(len(t_eval))]
    n_razd = num_trajectory

    for j in range(len(n_args)):
        for i in range(len(t_eval)):
            ee_mean[i][j] = ee1[i][j] / n_razd
            ee_absmean[i][j] = math.fabs(ee_mean[i][j])

    for j in range(len(n_args)):
        for i in range(len(t_eval)):
            for k in range(len(ee1[0])):
                ee_std[i][j] = math.sqrt((ee1[i][k]-ee_mean[i][j])**2/(n_razd - 1))

    return ee_mean, ee_absmean, ee_std, n_args


def friction_factor(args):
    f_f = np.zeros((5, 3))
    for i in range(f_f.shape[0]):
        for j in range(f_f.shape[1]):
            f_f[i, j] = 10 * args[j]*(i+j+1)**(j+1)
    return f_f


def scale_sample(sample, nom_vals, var):
    for i in range(sample.shape[0]):
        for j in range(sample.shape[2]):
            sample[i, :, j] = sample[i, :, j] * (nom_vals[j] * (1 + var) - nom_vals[j] * (1 - var)) + nom_vals[j] * (
                        1 - var)
    return sample



