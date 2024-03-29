# Generated by Django 4.1.5 on 2023-05-01 10:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kinetics", "0002_solutiondata_error_exp_point"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inputdata",
            name="initial_time",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(999999),
                ],
                verbose_name="Начальное время t0",
            ),
        ),
        migrations.AlterField(
            model_name="inputdata",
            name="step",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(999999),
                ],
                verbose_name="Шаг",
            ),
        ),
        migrations.AlterField(
            model_name="inputdata",
            name="time",
            field=models.FloatField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(999999),
                ],
                verbose_name="Время t",
            ),
        ),
        migrations.AlterField(
            model_name="solutiondata",
            name="error_exp_point",
            field=models.TextField(verbose_name="Погрешность в эксп. точках"),
        ),
    ]
