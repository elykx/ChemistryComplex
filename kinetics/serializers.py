from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError
from .models import TableParameters, InputData

class TableParametersSerializer(serializers.ModelSerializer):
    components = serializers.IntegerField(validators=[MinValueValidator(2, "Минимальное кол-во компонентов: 2"),
                                                      MaxValueValidator(20, "Максимальное кол-во компонентов: 20")])
    stages = serializers.IntegerField(validators=[MinValueValidator(1, "Минимальное кол-во стадий: 1"),
                                                      MaxValueValidator(20, "Максимальное кол-во стадий: 20")])
    experiments = serializers.IntegerField(validators=[MinValueValidator(1, "Минимальное кол-во экспериментов: 1"),
                                                      MaxValueValidator(20, "Максимальное кол-во экспериментов: 20")])
    class Meta:
        model = TableParameters
        fields = '__all__'


def matrix_stechiometric_validator(value):
    for row in value:
        for val in row:
            if val not in [-1,0,1]:
                raise ValidationError("Матрица стехиометрических коэффициентов принимает только -1, 0, 1")

class InputDataSerializer(serializers.ModelSerializer):
    initial_time = serializers.DecimalField(max_digits=10, decimal_places=6,
                                            validators=[MinValueValidator(0, "Минимальное начальное время: 0"),
                                                        MaxValueValidator(1000, "Максимальное начальное время: 1000")])
    time = serializers.DecimalField(max_digits=10, decimal_places=6,
                                    validators=[MinValueValidator(0, "Минимальное время: 0"),
                                                MaxValueValidator(1000, "Максимальное время: 1000")])
    step = serializers.DecimalField(max_digits=10, decimal_places=6,
                                    validators=[MinValueValidator(0, "Минимальный шаг: 0"),
                                                MaxValueValidator(1000, "Максимальный шаг: 1000")])
    matrix_stechiometric_coefficients = serializers.JSONField(validators=[matrix_stechiometric_validator])
    matrix_indicators = serializers.JSONField(validators=[MinValueValidator(0, "Минимальное значение показателя степени: 0"),
                                                          MaxValueValidator(10, "Максимальное значение показателя степени: 10")])
    experimental_data = serializers.JSONField(validators=[MinValueValidator(0, "Минимальное значение эксп. данных: 0"),
                                                          MaxValueValidator(1000, "Максимальное значение эксп. данных: 1000")])
    constants_speed = serializers.JSONField(validators=[MinValueValidator(0, "Минимальное значение констант скорости: 0"),
                                                          MaxValueValidator(10, "Максимальное значение констант скорости: 1000")])
    class Meta:
        model = InputData
        fields = '__all__'

