# coding: utf-8
# license: GPLv3
from typing import Callable

from typing import Tuple

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def _calc_ax(body, space_objects, local_x):
    """
    Calculates x-component of acceleration of the body caused by gravitation if it's x-coordinate would be local_x
    @param body: a space object for which an acceleration is calculated
    @param space_objects: a list of all space objects
    @param local_x: x-coordinate of position of the body
    @return: x-component of acceleration
    """
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


def _runge_kutta_calculation(x: float, vx: float, acceleration_function: Callable[[float], float], dt: float) \
        -> Tuple[float, float]:
    """
    Calculates next position and velocity of space object using Runge-Kutta method
    @param x: coordinate of space object along some axis at t=t
    @param vx: velocity along the same coordinate axis as x at t=t
    @param acceleration_function: a function x_cor -> acc_val that takes x-coordinate and returns an acceleration along
    the same coordinate axis if space object was at x_cor
    @param dt: an interval between this and next point in time
    @return: tuple (dx, dvx) of object's coordinate and velocity along the same coordinate axis at t=t+dt
    """
    k1x = dt * acceleration_function(x)
    q1x = dt * vx

    k2x = dt * acceleration_function(x + q1x / 2)
    q2x = dt * (vx + k1x / 2)

    k3x = dt * acceleration_function(x + q2x / 2)
    q3x = dt * (vx + k2x / 2)

    k4x = dt * acceleration_function(x + q3x)
    q4x = dt * (vx + k3x)

    velocity_delta = (k1x + 2 * k2x + 2 * k3x + k4x) / 6
    x_delta = (q1x + 2 * q2x + 2 * q3x + q4x) / 6
    return x_delta, velocity_delta


class SpaceObjectMotion:
    """
    Describes space object's change in coordinate and position between two points in time
    """
    def __init__(self, dx, dy, dvx, dvy):
        self.dx = dx
        self.dy = dy
        self.dvx = dvx
        self.dvy = dvy

    def apply(self, body):
        body.x += self.dx
        body.y += self.dy
        body.Vx += self.dvx
        body.Vy += self.dvy


def get_space_object_motion(body, space_objects, dt):
    """
    Calculates motion of the body during time interval dt
    @param body: a target space object
    @param space_objects: a list of all space objects on the scene
    @param dt: time interval between current and next time step
    @return: an object that describes change in position and velocity
    of the body between current and next points in time
    """
    ax = lambda x: _calc_ax(body, space_objects, x)
    dx, dvx = _runge_kutta_calculation(body.x, body.Vx, ax, dt)

    ay = lambda y: _calc_ay(body, space_objects, y)
    dy, dvy = _runge_kutta_calculation(body.y, body.Vy, ay, dt)
    return SpaceObjectMotion(dx, dy, dvx, dvy)


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    motions = []
    for body in space_objects:
        motions.append(get_space_object_motion(body, space_objects, dt))

    for body, motion in zip(space_objects, motions):
        motion.apply(body)


if __name__ == "__main__":
    print("This module is not for direct call!")
