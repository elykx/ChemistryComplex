import numpy as np
from pydiffeq import ODE_System


class System_ODE(ODE_System):
    def __init__(self, y0, matrix_stechiometric_coefficients, matrix_indicators, constants_speed):
        super().__init__(y0)
        self.matrix_stechiometric_coefficients = matrix_stechiometric_coefficients
        self.matrix_indicators = matrix_indicators
        self.constants_speed = constants_speed
        self.components = len(self.matrix_stechiometric_coefficients[0])
        self.stages = len(self.matrix_stechiometric_coefficients)

    def func(self, y, t):
        C = np.zeros(self.components)
        sumC = np.zeros(self.components)
        r = np.zeros(self.stages)
        sumR = np.zeros(self.stages)
        for i in range(self.stages):
            sumR[i] = self.constants_speed[i][0]
            for j in range(self.components):
                if self.matrix_indicators[i][j] != -1:
                    r[i] = y[j] ** self.matrix_indicators[i][j]
                    sumR[i] *= r[i]
        for i in range(self.components):
            for j in range(self.stages):
                C[i] = self.matrix_stechiometric_coefficients[j][i] * sumR[j]
                sumC[i] += C[i]
        return sumC
