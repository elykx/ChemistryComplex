from copy import copy

import numpy as np
from kinetics.sensetive.sensitivity_method import SensitivityMethod
from pydiffeq import ODE_Library


class MorrisMethod(SensitivityMethod):
    def __init__(self, solver, y0, t, num_trajectories, num_levels):
        """
        Инициализация метода Морриса.
        Parameters:
        - solver: решение мат. модели
        - t: время решения системы оду
        - y0: начальные значения системы оду
        - num_trajectories: количество траекторий для анализа чувствительности.
        - num_levels: количество уровней сетки
        """
        super().__init__(solver, t, y0)
        self.num_trajectories = num_trajectories
        self.num_levels = num_levels
        self.num_input = len(self.constants)

    def get_delta(self):
        """
        Функция для рассчета значения дельты для метода Морриса
        Parameters:
            num_levels - количество уровней (p) исходной сетки.
        Returns:
            дельта - значение используется для рассчета эл. эффектов
        """
        delta = self.num_levels / (2 * (self.num_levels - 1))
        return delta

    def get_x_star(self):
        """
        Функция для получения вектора x
        Parameters:
            num_levels - количество уровней исходной сетки
            num_input - количество входных параметров
            delta - значение используется для рассчета эл. эффектов
        Returns:
            x_star - basis vector / starting for the Morris trajectories
        """
        delta = self.get_delta()
        grid = np.linspace(0, 1 - delta, int(self.num_levels / 2))
        x_star = np.random.choice(grid, size=self.num_input)
        return x_star

    def compute_Bstar(self):
        """
        Function for obtaining a sample trajectory in form of B*.
        Parameters:
            num_input - number of input factors of the model
            delta - increment to be used when obtaining elementary effects
            x_star - starting points for the Morris trajectories

        Returns:
            B_star - a sample trajectory for Morris method.
        """
        k = self.num_input
        delta = self.get_delta()
        x_star = self.get_x_star()

        # Obtain strictly lower triangular matrix
        B = np.tril(np.ones((k + 1, k)), -1)

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

    def morris_sample(self):
        """
        Function for generating sample trajectories for Morris method of Elementary Effects.

        Parameters:
            num_input - number of input factors of the model
            n_trajectories - number of trajectories to be calculated
            num_levels - number of levels in the grid space

        Returns:
            B_star - a sample trajectory for Morris method.
        """
        k = self.num_input
        delta = self.get_delta()

        morris_sample = np.zeros([self.num_trajectories, k + 1, k])

        for i in range(self.num_trajectories):
            x_star = self.get_x_star()

            morris_sample[i, :, :] = self.compute_Bstar()

        return morris_sample

    def scale_sample(self):
        """
        Function for scaling a Morris sample for Elementary Effects.
        Currently only supports scaling a uniform distribution.

        Parameters:
            sample - sample trajectories generated via Morris method
            nom_vals - nominal values to be used for scaling
            var - variation around the norminal values to be used for scaling

        Returns:
            sample - scaled Morris sample trajectories for elementary effects method.
        """
        sample = self.morris_sample()
        var = 0.25

        for i in range(sample.shape[0]):
            for j in range(sample.shape[2]):
                sample[i, :, j] = sample[i, :, j] * (self.constants[j][0] * (1 + var) - self.constants[j][0] *
                                                     (1 - var)) + self.constants[j][0] * (1 - var)

        return sample

    def elementary_effects(self):
        """
        Function for calculating Elementary Effects.

        Parameters:
            sample - sample trajectories generated via Morris method
            model - function to be used to generate outputs
            delta - increment to be used when obtaining elementary effects

        Returns:
            ee_mean - means of elementary effects for each factor (known as mu)
            ee_absmean - means of absolute elementary effects for each factor (known as mu_star)
            ee_std - standard deviation of elementary effects for each factor (known as sigma^2)
        """
        delta = self.get_delta()
        sample = self.scale_sample()
        base_model = copy(self.solver.system)

        y = np.zeros((sample.shape[0], sample.shape[1]))
        ee = np.zeros((sample.shape[0], sample.shape[2], len(self.t)))

        for i in range(sample.shape[0]):
             for j in range(sample.shape[1] - 1):
                args1 = sample[i, j]
                args2 = sample[i, j+1]
                base_model.constants_speed = args1.reshape(-1, 1).tolist()
                solve1 = ODE_Library(base_model, self.method).solve(self.t, self.y0)
                base_model.constants_speed = args2.reshape(-1, 1).tolist()
                solve2 = ODE_Library(base_model, self.method).solve(self.t, self.y0)
                for k in range(sample.shape[2]):
                    if args2[k] > args1[k]:
                        ee[i, j, :] = (solve2.transpose() - solve1.transpose()) / (2 * delta)
                    elif args2[k] < args1[k]:
                        ee[i, j, :] = (solve2.transpose() - solve1.transpose()) / (2 * delta)

        ee = np.zeros((sample.shape[0], sample.shape[2]))

        for i in range(sample.shape[0]):
            for j in range(sample.shape[1] - 1):
                for k in range(sample.shape[2]):
                    if sample[i, j + 1, k] > sample[i, j, k]:
                        ee[i, k] = (y[i, j + 1] - y[i, j]) / delta
                    elif sample[i, j + 1, k] < sample[i, j, k]:
                        ee[i, k] = (y[i, j] - y[i, j + 1]) / delta

        ee_mean = [np.mean(ee[:, i]) for i in range(ee.shape[1])]
        ee_absmean = [np.mean(np.abs(ee[:, i])) for i in range(ee.shape[1])]
        ee_std = [np.std(ee[:, i]) for i in range(ee.shape[1])]

        return ee_mean, ee_absmean, ee_std

    def calculate_sensitivity(self):
        # """
        # Вычисление чувствительности
        # """
        # num_constants = len(self.constants)
        #
        # delta = num_constants / (2 * (num_constants - 1))
        #
        # grid = np.linspace(0, 1 - delta, int(num_constants / 2))
        # x_star = np.random.choice(grid, size=num_constants)

        # result = np.zeros((num_constants, self.step))
        # base_model = copy(self.solver.system)
        # cal_model = copy(self.solver.system)
        #
        # for i in range(self.step):
        #     p = np.random.randint(0, num_constants)
        #     sign = np.random.choice([-1, 1])
        #     params_perturbed = copy(self.constants)
        #     params_perturbed[p] += sign * self.step_size
        #
        #
        #     base_solution = ODE_Library(base_model, self.method).solve(self.t, self.y0)
        #     perturbed_solution = ODE_Library(cal_model, self.method).solve(self.t, self.y0)
        #
        #     result[p][i] = (perturbed_solution[p][i] - base_solution[p][i]) / self.step_size

        return 0
