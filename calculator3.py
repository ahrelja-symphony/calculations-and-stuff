from math import sqrt

from numba import njit, prange

import numpy as np


@njit
def calculate_distance(current_point, input_point):
    res1 = (
        (current_point[0] - input_point[0]) * (current_point[0] - input_point[0])
        + (current_point[1] - input_point[1]) * (current_point[1] - input_point[1])
        + (current_point[2] - input_point[2]) * (current_point[2] - input_point[2])
    )
    res2 = sqrt(res1)
    return res2


@njit
def calculate_contribution(distance, propagation_factor, intensity_factor):
    return intensity_factor / ((1 + distance) ** propagation_factor)


@njit
def calculate_value(current_point, holes, propagation_factor, intensity_factor):
    total_contribution = 0

    for holes in holes:
        for h in range(holes[2] - holes[3] // 2, holes[2] + holes[3] // 2):
            distance = calculate_distance(current_point=current_point, input_point=(holes[0], holes[1], h))
            total_contribution += calculate_contribution(
                distance=distance, propagation_factor=propagation_factor, intensity_factor=intensity_factor
            )

    return total_contribution


class Calculator:
    def __init__(self, x_range, y_range, z_range, propagation_factor, intensity_factor):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.propagation_factor = propagation_factor
        self.intensity_factor = intensity_factor

    def get_output(self, holes):
        holes_tuples = np.array([(hole.x, hole.y, hole.z, hole.height) for hole in holes])

        output_matrix = self.__initialize_output_matrix()
        output_matrix = self.__calculate_outputs(output_matrix, holes_tuples, self.propagation_factor, self.intensity_factor)

        return (
            self.__flatten_by_x(output_matrix),
            self.__flatten_by_y(output_matrix),
            self.__flatten_by_z(output_matrix),
        )

    def __initialize_output_matrix(self):
        output_matrix = np.zeros((self.x_range, self.y_range, self.z_range))

        return output_matrix

    @staticmethod
    @njit(parallel=True)
    def __calculate_outputs(output_matrix, holes, propagation_factor, intensity_factor):
        x_range = output_matrix.shape[0]
        y_range = output_matrix.shape[1]
        z_range = output_matrix.shape[2]
        for x in prange(x_range):
            for y in prange(y_range):
                for z in prange(z_range):
                    output_matrix[x][y][z] = calculate_value(
                        current_point=(x, y, z),
                        holes=holes,
                        propagation_factor=propagation_factor,
                        intensity_factor=intensity_factor,
                    )

        return output_matrix

    @staticmethod
    @njit(parallel=True)
    def __flatten_by_x(matrix):
        flattened_output = np.zeros((matrix.shape[1], matrix.shape[2]))

        for y in prange(matrix.shape[1]):
            for z in prange(matrix.shape[2]):
                flattened_value = 0.0
                for x in prange(matrix.shape[0]):
                    flattened_value += matrix[x][y][z]

                flattened_output[y][z] = flattened_value

        return flattened_output

    @staticmethod
    @njit(parallel=True)
    def __flatten_by_y(matrix):
        flattened_output = np.zeros((matrix.shape[0], matrix.shape[2]))

        for x in prange(matrix.shape[0]):
            for z in prange(matrix.shape[2]):
                flattened_value = 0.0
                for y in prange(matrix.shape[1]):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][z] = flattened_value

        return flattened_output

    @staticmethod
    @njit(parallel=True)
    def __flatten_by_z(matrix):
        flattened_output = np.zeros((matrix.shape[0], matrix.shape[1]))

        for x in prange(matrix.shape[0]):
            for y in prange(matrix.shape[1]):
                flattened_value = 0.0
                for z in prange(matrix.shape[2]):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][y] = flattened_value

        return flattened_output
