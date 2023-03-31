from enum import Enum


class MethodName(Enum):
    EXPLICIT_EULER = 'EXPLICIT_EULER'
    IMPLICIT_EULER = 'IMPLICIT_EULER'
    SEMI_IMPLICIT_EULER = 'SEMI_IMPLICIT_EULER'
    TRAPEZOID = 'TRAPEZOID'
    MIDDLE = 'MIDDLE'
    EXPLICIT_RK2 = 'EXPLICIT_RK2'
    IMPLICIT_RK2 = 'IMPLICIT_RK2'
    SEMI_IMPLICIT_RK2 = 'SEMI_IMPLICIT_RK2'
    EXPLICIT_RK4 = 'EXPLICIT_RK4'
    IMPLICIT_RK4 = 'IMPLICIT_RK4'
    SEMI_IMPLICIT_RK4 = 'SEMI_IMPLICIT_RK4'
    KM = 'KM'
    RKF = 'RKF'
    EXPLICIT_ADAMS = 'EXPLICIT_ADAMS'


METHOD_CHOICES = [
    (MethodName.EXPLICIT_EULER.value, 'Явный метод Эйлера'),
    (MethodName.IMPLICIT_EULER.value, 'Неявный метод Эйлера'),
    (MethodName.SEMI_IMPLICIT_EULER.value, 'Полу-неявный метод Эйлера'),
    (MethodName.TRAPEZOID.value, 'Метод трапеций'),
    (MethodName.MIDDLE.value, 'Метод средней точки'),
    (MethodName.EXPLICIT_RK2.value, 'Явный метод Рунге-Кутты 2-го порядка'),
    (MethodName.IMPLICIT_RK2.value, 'Неявный метод Рунге-Кутты 2-го порядка'),
    (MethodName.SEMI_IMPLICIT_RK2.value, 'Полу-неявный метод Рунге-Кутты 2-го порядка'),
    (MethodName.EXPLICIT_RK4.value, 'Явный метод Рунге-Кутты 4-го порядка'),
    (MethodName.IMPLICIT_RK4.value, 'Неявный метод Рунге-Кутты 4-го порядка'),
    (MethodName.SEMI_IMPLICIT_RK4.value, 'Полу-неявный метод Рунге-Кутты 4-го порядка'),
    (MethodName.KM.value, 'Метод Кутты-Мерсона'),
    (MethodName.RKF.value, 'Метод Рунге-Кутты-Фелберга'),
    (MethodName.EXPLICIT_ADAMS.value, 'Явный двухшаговый метод Адамса'),
]