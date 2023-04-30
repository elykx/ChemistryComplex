from django.core.exceptions import ValidationError


def stechiometric_validator(value):
    value = value.replace("[", "").replace("]", "")
    value = value.replace('"', "").replace('"', "")
    numbers = [row.split(',') for row in value.split(';')]
    numbers = [[float(num) for num in row] for row in numbers]
    for row in numbers:
        for num in row:
            if num not in [-1, 0, 1]:
                raise ValidationError("Матрица стехиометрических коэффициентов принимает только -1, 0, 1")


def matrix_indicators_validator(value):
    value = value.replace("[", "").replace("]", "")
    value = value.replace('"', "").replace('"', "")
    numbers = [row.split(',') for row in value.split(';')]
    numbers = [[float(num) for num in row] for row in numbers]
    for row in numbers:
        for num in row:
            if num < -1 or num > 1000:
                raise ValidationError("Number not in range")


def min_max_validator(value):
    value = value.replace("[", "").replace("]", "")
    value = value.replace('"', "").replace('"', "")
    numbers = [row.split(',') for row in value.split(';')]
    numbers = [[float(num) for num in row] for row in numbers]
    for row in numbers:
        for num in row:
            if num < 0 or num > 1000:
                raise ValidationError("Number not in range [0, 100]")
