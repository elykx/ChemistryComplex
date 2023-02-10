# Generated by Django 4.1.5 on 2023-02-07 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kinetics', '0009_alter_solutiondata_experimental_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdata',
            name='table_parameters',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='kinetics.tableparameters', verbose_name='Параметры таблицы'),
        ),
    ]
