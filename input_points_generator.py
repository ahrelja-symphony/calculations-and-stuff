import random
from dataclasses import dataclass


@dataclass
class Hole:
    x: int
    y: int
    z: int
    height: float


class HolesGenerator:
    @staticmethod
    def get_random(number_of_points, x_range, y_range, z_range):
        return [
            Hole(
                x=random.randint(0, x_range),
                y=random.randint(0, y_range),
                z=random.randint(0, z_range),
                height=random.uniform(1, 10),
            )
            for _ in range(number_of_points)
        ]

    @staticmethod
    def get_diagonal(step, x_range, y_range, z_range, height):
        return [Hole(x=i, y=i, z=i, height=height) for i in range(0, min((x_range, y_range, z_range)), step)]

    @staticmethod
    def get_surface_row(step, x_range, y_range, z_range, height):
        y = y_range // 2
        z = z_range - height // 2

        return [Hole(x=x, y=y, z=z, height=height) for x in range(0, x_range, step)]
