# Generated by Django 4.1.5 on 2023-05-07 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kinetics", "0002_solutiondata_error_exp_point"),
    ]

    operations = [
        migrations.AlterField(
            model_name="solutiondata",
            name="error_exp_point",
            field=models.TextField(verbose_name="Погрешность в эксп. точках"),
        ),
    ]
