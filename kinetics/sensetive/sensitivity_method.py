from abc import ABC, abstractmethod


class SensitivityMethod(ABC):
    def __init__(self, solver, t, y0):
        """
        Инициализация метода оценки чувствительности.

        Parameters:
        - model: модель процесса
        - constants: массив с исходными константами, которые используются при решении модели.
        - t: время решения системы оду
        - y0: начальные значения системы оду
        """
        self.solver = solver
        self.constants = self.solver.system.constants_speed
        self.method = self.solver.method
        self.t = t
        self.y0 = y0

    @abstractmethod
    def calculate_sensitivity(self):
        """
         Абстрактный метод для вычисления чувствительности.
        """
        pass
