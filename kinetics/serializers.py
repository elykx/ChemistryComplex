from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError
from .models import TableParameters, InputData, SolutionData


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
    value = value.replace("[", "").replace("]", "")
    numbers = [row.split(',') for row in value.split(';')]
    numbers = [[float(num) for num in row] for row in numbers]
    for row in numbers:
        for num in row:
            if num not in [-1, 0, 1]:
                raise ValidationError("Матрица стехиометрических коэффициентов принимает только -1, 0, 1")


def min_max_matrix_validator(value):
    value = value.replace("[", "").replace("]", "")
    numbers = [row.split(',') for row in value.split(';')]
    numbers = [[float(num) for num in row] for row in numbers]
    for row in numbers:
        for num in row:
            if num < 0 or num > 1000:
                raise ValidationError("Number not in range [0, 100]")


class InputDataSerializer(serializers.ModelSerializer):
    initial_time = serializers.FloatField(validators=[MinValueValidator(0, "Минимальное начальное время: 0"),
                                                        MaxValueValidator(1000, "Максимальное начальное время: 1000")])
    time = serializers.FloatField(validators=[MinValueValidator(0, "Минимальное время: 0"),
                                                MaxValueValidator(1000, "Максимальное время: 1000")])
    step = serializers.FloatField(validators=[MinValueValidator(0, "Минимальный шаг: 0"),
                                                MaxValueValidator(1000, "Максимальный шаг: 1000")])

    matrix_stechiometric_coefficients = serializers.CharField(validators=[matrix_stechiometric_validator])
    matrix_indicators = serializers.CharField(validators=[min_max_matrix_validator])
    experimental_data = serializers.CharField(validators=[min_max_matrix_validator])
    constants_speed = serializers.CharField(validators=[min_max_matrix_validator])


    class Meta:
        model = InputData
        fields = '__all__'


class SolutionDataSerializer(serializers.ModelSerializer):
    input_data = InputDataSerializer(many=False, read_only=True)

    class Meta:
        model = SolutionData
        fields = ('id', 'input_data', 'result', 'time', 'experimental_point')
