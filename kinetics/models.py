from django.db import models
from django.core import validators

class TableParameters(models.Model):
    components = models.IntegerField(verbose_name='Количество компонентов')
    stages = models.IntegerField(verbose_name='Количество стадий')
    experiments = models.IntegerField(verbose_name='Количество экспериментов')


class InputData(models.Model):
    initial_time = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='Начальное время t0')
    time = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='Время t')
    step = models.DecimalField(max_digits=10, decimal_places=6, verbose_name= 'Шаг')
    matrix_stechiometric_coefficients = models.JSONField(verbose_name='Матрица стехиометрических коэффициентов')
    matrix_indicators = models.JSONField(verbose_name='Матрица показателей степени')
    experimental_data = models.JSONField(verbose_name='Экспериментальные данные')
    constants_speed = models.JSONField(verbose_name='Константы скорости')

    EULER = 'EULER'
    IMPLICIT_EULER = 'IMPLICIT_EULER'
    TRAPEZOID = 'TRAPEZOID'
    MIDDLE = 'MIDDLE'
    RK2 = 'RK2'
    RK4 = 'RK4'
    KM = 'KM'
    RKF = 'RKF'
    EXPLICIT_ADAMS = 'EXPLICIT_ADAMS'
    METHOD_CHOICES = [
        (EULER, 'Метод Эйлера'),
        (IMPLICIT_EULER, 'Неявный метод Эйлера'),
        (TRAPEZOID, 'Метод трапеций'),
        (MIDDLE, 'Метод средней точки'),
        (RK2, 'Метод Рунге-Кутты 2-го порядка'),
        (RK4, 'Метод Рунге-Кутты 4-го порядка'),
        (KM, 'Метод Кутты-Мерсона'),
        (RKF, 'Метод Рунге-Кутты-Фелберга'),
        (EXPLICIT_ADAMS, 'Явный двухшаговый метод Адамса'),
    ]
    method = models.CharField(max_length=255,
                                    choices=METHOD_CHOICES,
                                    default=EULER,
                                    verbose_name="Метод решения")
