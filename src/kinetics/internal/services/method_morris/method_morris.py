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


def elementary_effects(sample, solution, delta):
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

    ee = copy.deepcopy(y)

    for i in range(len(s)):
        for j in range(len(s[i])-1):
            for k in range(len(s[i][j])):
                for tt in range(len(y[i][j])):
                    if s[i][j][k] > s[i][j - 1][k]:
                        y1 = y[i][j+1][tt]
                        y2 = y[i][j][tt]
                        e = (y1-y2) / delta
                        ee[i][j][tt] = e
                    else:
                        y1 = y[i][j+1][tt]
                        y2 = y[i][j][tt]
                        e = (y2-y1) / delta
                        ee[i][j][tt] = e
    n_args = []
    for i in range(len(constants_speed)):
       n_args.append(i+1)

    ee_mean = [[0] * len(t_eval)] * len(n_args)
    ee_absmean = [[0] * len(t_eval)] * len(n_args)
    ee_std = [[0] * len(t_eval)] * len(n_args)
    n_razd = [0]*len(n_args)

    for q in range(len(n_args)):
        for k in range(len(numberofconst)):
            if numberofconst[k] == n_args[q]:
                for i in range(len(ee)):
                    for mn in range(len(t_eval)):
                        ee_mean[q][mn] += ee[i][q][mn]
                        n_razd[q] += 1



    for j in range(len(ee[0]) - 1):
        for q in range(len(n_args)):
            print(ee_mean, n_razd)
            ee_mean[j][q] = sum(ee_mean[j][q]) / n_razd[q]
            ee_absmean[j][q] = math.fabs(ee_mean[j][q])

    print(ee_mean)
    for i in range(len(ee)):
        for j in range(len(ee[i]) - 1):
            for q in range(len(n_args)):
                for k in range(len(numberofconst)):
                    if numberofconst[k] == n_args[q]:
                        ee_std[j][q] = ((sum(ee[i][q][j])-ee_mean[j][q])**2)/(n_razd[q]-1)

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



