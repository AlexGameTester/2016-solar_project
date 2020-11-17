from solar_model import gravitational_constant
import itertools


class StatisticsWatcher:
    """
    Class that calculates and stores different type of statistical data about space objects
    """

    def __init__(self, current_time):
        """
        Creates StatisticsWatcher instance
        @param current_time: time when calculations started. Statistics about this moment is not calculated
        """
        self.current_time = current_time
        self.time_array = []
        self.energy_array = []

    def _calculate_energy(self, space_objects):
        energy = 0
        for obj in space_objects:
            v_sq = obj.Vx ** 2 + obj.Vy ** 2
            energy += 1 / 2 * obj.m * v_sq

        for obj1, obj2 in itertools.combinations(space_objects, 2):
            r = ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** (1 / 2)
            if r == 0:
                r = obj1.R + obj2.R
                # if objects are very close to each other they will touch, but not go through each other
            energy += -gravitational_constant * obj1.m * obj2.m / r

        return energy

    def _update_energy(self, space_objects):
        self.energy_array.append(self._calculate_energy(space_objects))

    def calculate_statistics(self, space_objects, **kwargs):
        """
        Calculates and saves statistics about this point in time
        @param space_objects: array of space objects on the scene
        @keyword dt: a time interval between previous and this point in time.
        Exactly one keyword from list [dt, current_time] must be used
        @keyword current_time: time when calculation is executed.
        Exactly one keyword from list [dt, current_time] must be used
        """
        keys = kwargs.keys()
        if 'dt' in keys and 'current_time' in keys:
            raise ValueError('Keyword arguments should contain dt or current_time, but not both of them')
        elif 'dt' in keys:
            dt = kwargs['dt']
            self.current_time += dt
            self.time_array.append(self.current_time)
            self._update_energy(space_objects)
        elif 'current_time' in keys:
            current_time = kwargs['current_time']
            self.current_time = current_time
            self.time_array.append(current_time)
            self._update_energy(space_objects)
        else:
            raise ValueError('Keyword arguments must contain either dt or current_time')
