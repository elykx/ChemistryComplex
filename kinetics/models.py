from django.db import models


class TableParameters(models.Model):
    components = models.IntegerField(verbose_name='Количество компонентов')
    stages = models.IntegerField(verbose_name='Количество стадий')
    experiments = models.IntegerField(verbose_name='Количество экспериментов')


class InputData(models.Model):
    table_parameters = models.ForeignKey(TableParameters, on_delete=models.CASCADE, verbose_name="Параметры таблицы")
    initial_time = models.FloatField(verbose_name='Начальное время t0')
    time = models.FloatField(verbose_name='Время t', )
    step = models.FloatField(verbose_name='Шаг')
    matrix_stechiometric_coefficients = models.TextField(verbose_name='Матрица стехиометрических коэффициентов')
    matrix_indicators = models.TextField(verbose_name='Матрица показателей степени')
    experimental_data = models.TextField(verbose_name='Экспериментальные данные')
    constants_speed = models.TextField(verbose_name='Константы скорости')

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


class SolutionData(models.Model):
    input_data = models.ForeignKey(InputData, on_delete=models.CASCADE, verbose_name="Входные данные")
    result = models.TextField(verbose_name="Данные, расчитанные выбранным методом")
    experimental_point = models.TextField(verbose_name="Значение в эксп. точках")
    time = models.TextField(verbose_name="Время")

