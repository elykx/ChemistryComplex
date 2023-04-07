from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TableParameters(models.Model):
    components = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(20)],
                                     verbose_name='Количество компонентов')
    stages = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)],
                                 verbose_name='Количество стадий')
    experiments = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)],
                                      verbose_name='Количество экспериментов')

    def __str__(self):
        return f"components: {self.components}, stages:{self.stages}, experoments: {self.experiments}"

    class Meta:
        verbose_name = "Table Parameters"
