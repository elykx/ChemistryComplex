# Комплекс для решения задачи химической кинетики

## Технологии
    Python v.3.10, Django v4.1

## Переменные окружения
    .env
    DEBUG=True
    SECRET_KEY=

## REST API

### Create Table parameters

- POST `api/v1/kinetics/tableparameters/`

### Get Table parameters

- GET `api/v1/kinetics/tableparameters/<int: index>`

### Create Input Data

- POST `api/v1/kinetics/inputdata/`

### Get Input Data

- GET `api/v1/kinetics/inputdata/<int: index>`

### Get Solution Data

- GET `api/v1/kinetics/solutiondata/<int: index>`

### Save Excel Report

- GET `api/v1/kinetics/solutiondata/save/<int: index>`
