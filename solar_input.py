# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet, ObjectType
import re


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename, encoding='cp1251') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            try:
                obj = parse_object_parameters(line)
                objects.append(obj)
            except ValueError:
                print('Incorrect line format')

            else:
                print("Unknown space object")

    return objects


def parse_object_parameters(line: str):
    """
    Reads space object parameters from string line
    Входная строка должна иметь слеюущий формат:
    Star/Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    @param line: a string that describes object
    @raise ValueError: raised is line format is incorrect
    """
    pattern = r'(Star|Planet)\s+([0-9.,eE\-]+)\s+(\w+)\s+([0-9.,eE\-]+)\s+([0-9.,eE\-]+)\s+([0-9.,eE\-]+)\s+([0-9.,' \
              r'eE\-]+)\s+([0-9.,eE\-]+)\s+\n?'

    match = re.match(pattern, line)
    if match is None:
        raise ValueError('Line format is not correct')

    obj = None

    obj_type = match.group(1)
    if obj_type == 'Star':
        obj = Star()
    elif obj_type == 'Planet':
        obj = Planet()
    else:  # must never occur, but still
        raise ValueError('Line format is not correct')

    radius = float(match.group(2))
    if radius < 0:
        raise ValueError('Line format is not correct')
    else:
        obj.R = radius

    color = match.group(3)
    obj.color = color

    mass = float(match.group(4))
    if mass < 0:
        raise ValueError('Line format is not correct')
    else:
        obj.m = mass

    x = float(match.group(5))
    obj.x = float(x)

    y = float(match.group(6))
    obj.y = float(y)

    vx = float(match.group(7))
    obj.Vx = float(vx)

    vy = float(match.group(8))
    obj.Vy = float(vy)

    return obj


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            if type(obj) is Star: 
                out_file.write("Star" + " " + "{:e} {} {:e} {:e} {:e} {:e} {:e}".format(obj.R, obj.color, obj.m, 
                               obj.x,obj.y, obj.Vx, obj.Vy) + "\n")
                
            elif type(obj) is Planet:
                out_file.write("Planet" + " " + "{:e} {} {:e} {:e} {:e} {:e} {:e}".format(obj.R, obj.color, obj.m, 
                               obj.x,obj.y, obj.Vx, obj.Vy) + "\n")
            else :
                print("GG")                                      
            

# FIXME: хорошо бы ещё сделать функцию, сохранающую статистику в заданный файл...


if __name__ == "__main__":
    print("This module is not for direct call!")
