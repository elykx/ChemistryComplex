from django.db import models

from kinetics.internal.models.input_data import InputData


class SolutionData(models.Model):
    input_data = models.ForeignKey(InputData, on_delete=models.CASCADE, verbose_name="Входные данные")
    result = models.TextField(verbose_name="Данные, расчитанные выбранным методом")
    experimental_point = models.TextField(verbose_name="Значение в эксп. точках")
    time = models.TextField(verbose_name="Время")
    error_exp_point = models.TextField(verbose_name="Погрешность в эксп. точках")
    runtime = models.FloatField(verbose_name='Время выполнения', default=None)

    def __str__(self):
        return f"Input data: {self.input_data}, result:{self.result}, experimental points: {self.experimental_point}" \
               f"time: {self.time}"

    class Meta:
        verbose_name = "Solution Data"
