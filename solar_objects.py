# coding: utf-8
# license: GPLv3
from enum import Enum
from abc import ABC


class ObjectType(Enum):
    star = 1
    planet = 2


class SpaceObject(ABC):
    """
    Represents a space object that moves due to the force of gravity
    """
    m = 0
    """Масса тела"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус тела"""

    color = "red"
    """Цвет тела"""

    image = None
    """Изображение тела"""


class Star(SpaceObject):
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """
    def __init__(self):
        self.type = ObjectType.star


class Planet(SpaceObject):
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """
    def __init__(self):
        self.type = ObjectType.planet


