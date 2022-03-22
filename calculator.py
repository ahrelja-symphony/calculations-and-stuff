from math import sqrt

import numpy as np
from numba import njit, jit, prange


@njit
def calculate_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


@njit
def calculate_contribution(distance):
    return 10000 / ((1 + distance) ** 4)


@njit
def calculate_value(current_point, input_points):
    max_distance = 0

    for input_point in input_points:
        distance = calculate_distance(
          p1=current_point, p2=input_point
        )

        if distance > max_distance:
            max_distance = distance

    return calculate_contribution(distance=max_distance)


class Calculator:
    def __init__(self, x_range, y_range, z_range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def get_output(self, input_points):
        input_points_np = np.array(input_points)
        output_matrix = self.__initialize_output_matrix()
        output_matrix = self.__calculate_outputs(output_matrix, input_points_np)
        flattened_output = self.__flatten(output_matrix)

        return flattened_output

    def __initialize_output_matrix(self):
        return np.zeros((self.x_range, self.y_range, self.z_range))

    @staticmethod
    @jit(nopython=False, parallel=True)
    def __calculate_outputs(output_matrix, input_points):
        for x in prange(output_matrix.shape[0]):
            for y in prange(output_matrix.shape[1]):
                for z in prange(output_matrix.shape[2]):
                    output_matrix[x][y][z] = calculate_value(
                        current_point=(x, y, z), input_points=input_points
                    )

        return output_matrix

    @staticmethod
    @jit(nopython=False, parallel=True)
    def __flatten(matrix):
        flattened_output = np.zeros((matrix.shape[0], matrix.shape[1]))

        for x in prange(matrix.shape[0]):
            for y in prange(matrix.shape[0]):
                flattened_value = 0
                for z in prange(matrix.shape[0]):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][y] = flattened_value

        return flattened_output
