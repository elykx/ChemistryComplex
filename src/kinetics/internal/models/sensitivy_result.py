from django.db import models


class SensitivityResult(models.Model):
    average = models.TextField(verbose_name="Среднее значение")
    absolute_average = models.TextField(verbose_name="Абсолютное среднее значение")
    standart_deviation = models.TextField(verbose_name="Стандартное отклонение")
    constant_speed_num = models.TextField(verbose_name="Нумерация констант скорости")

    class Meta:
        verbose_name = "Sensitivity Result"