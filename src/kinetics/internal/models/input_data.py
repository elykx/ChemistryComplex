from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from kinetics.internal.models.table_parameters import TableParameters
from kinetics.internal.models.validators.matrix_validators import min_max_validator, stechiometric_validator
from kinetics.internal.models.validators.methods_name import METHOD_CHOICES, MethodName


class InputData(models.Model):
    table_parameters = models.ForeignKey(TableParameters, on_delete=models.CASCADE, verbose_name="Параметры таблицы")
    initial_time = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)],
                                     verbose_name='Начальное время t0')
    time = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)],
                             verbose_name='Время t', )
    step = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)],
                             verbose_name='Шаг')
    matrix_stechiometric_coefficients = models.TextField(validators=[stechiometric_validator], verbose_name='Матрица стехиометрических коэффициентов')
    matrix_indicators = models.TextField(validators=[min_max_validator], verbose_name='Матрица показателей степени')
    experimental_data = models.TextField(validators=[min_max_validator], verbose_name='Экспериментальные данные')
    constants_speed = models.TextField(validators=[min_max_validator], verbose_name='Константы скорости')
    method = models.CharField(max_length=255,
                              choices=METHOD_CHOICES,
                              default=MethodName.EXPLICIT_EULER.value,
                              verbose_name="Метод решения")

    def __str__(self):
        return f"table parameters: {self.table_parameters}, initial time: {self.initial_time}, time: {self.time}," \
               f" step: {self.step}"

    class Meta:
        verbose_name = "Input Data"
