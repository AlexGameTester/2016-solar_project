# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects, local_x, local_y):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    fx = 0
    fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r_x = ((local_x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        r_y = ((body.x - obj.x)**2 + (local_y - obj.y)**2)**0.5
        fx += gravitational_constant * body.m * obj.m / r_x**3 * (obj.x - local_x)
        fy += gravitational_constant * body.m * obj.m / r_y**3 * (obj.y - local_y)

    return (fx, fy)


def _calc_ax(body, space_objects, local_x):
    ax = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r_x = ((local_x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        ax += gravitational_constant * obj.m / r_x**3 * (obj.x - local_x)

    return ax


def _calc_ay(body, space_objects, local_y):
    ay = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r_y = ((body.x - obj.x)**2 + (local_y - obj.y)**2)**0.5
        ay += gravitational_constant * obj.m / r_y**3 * (obj.y - local_y)

    return ay


def move_space_object_rk(body, space_objects, dt):
    ax = lambda x: _calc_ax(body, space_objects, x)
    k1x = dt * ax(body.x)
    q1x = dt * body.Vx

    k2x = dt * ax(body.x + q1x / 2)
    q2x = dt * (body.Vx + k1x / 2)

    k3x = dt * ax(body.x + q2x / 2)
    q3x = dt * (body.Vx + k2x / 2)

    k4x = dt * ax(body.x + q3x)
    q4x = dt * (body.Vx + k3x)

    body.Vx += (k1x + 2 * k2x + 2 * k3x + k4x) / 6
    body.x += (q1x + 2 * q2x + 2 * q3x + q4x) / 6

    ay = lambda y: _calc_ay(body, space_objects, y)
    k1y = dt * ay(body.y)
    q1y = dt * body.Vy

    k2y = dt * ay(body.y + q1y / 2)
    q2y = dt * (body.Vy + k1y / 2)

    k3y = dt * ay(body.y + q2y / 2)
    q3y = dt * (body.Vy + k2y / 2)

    k4y = dt * ay(body.y + q3y)
    q4y = dt * (body.Vy + k3y)

    body.Vy += (k1y + 2 * k2y + 2 * k3y + k4y) / 6
    body.y += (q1y + 2 * q2y + 2 * q3y + q4y) / 6



def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """

    ax = body.Fx / body.m
    ay = body.Fy / body.m
    body.x += body.Vx * dt
    body.Vx += ax*dt

    body.y += body.Vy * dt
    body.Vy += ay*dt


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        move_space_object_rk(body, space_objects, dt)

    # for body in space_objects:
    #     calculate_force(body, space_objects)
    # for body in space_objects:
    #     move_space_object(body, dt)


if __name__ == "__main__":
    print("This module is not for direct call!")
