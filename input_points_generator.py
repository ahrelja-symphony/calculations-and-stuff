import random


class InputPointGenerator:
    @staticmethod
    def get_random(number_of_points, x_range, y_range, z_range):
        return (
            (random.randint(0, x_range), random.randint(0, y_range), random.randint(0, z_range))
            for _ in range(number_of_points)
        )

    @staticmethod
    def get_diagonal(step, x_range, y_range, z_range):
        return ((i, i, i) for i in range(0, min((x_range, y_range, z_range)), step))
