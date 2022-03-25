import random

from hole import Hole


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

    @staticmethod
    def get_surface_diagonal_cross(step, x_range, y_range, z_range, height):
        z = z_range - height // 2

        main_diagonal = [Hole(x=i, y=i, z=z, height=height) for i in range(0, min(x_range, y_range), step)]
        secondary_diagonal = [Hole(x=i, y=y_range - i, z=z, height=height) for i in range(0, min(x_range, y_range), step)]
        print(main_diagonal)
        print(secondary_diagonal)
        return main_diagonal + secondary_diagonal
