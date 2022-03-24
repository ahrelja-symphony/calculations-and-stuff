from math import sqrt

import numpy as np
from numba import njit, jit, prange


@njit
def calculate_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


@njit
def calculate_contribution(distance, propagation_factor, intensity_factor):
    return intensity_factor / ((1 + distance) ** propagation_factor)


@njit
def calculate_value(current_point, input_points, propagation_factor, intensity_factor):
    total_contribution = 0.0

    for input_point in input_points:
        for h in range(input_point[2] - input_point[3] // 2, input_point[2] + input_point[3] // 2):
            distance = calculate_distance(p1=current_point, p2=(input_point[0], input_point[1], h))
            contribution = calculate_contribution(
                distance=distance, propagation_factor=propagation_factor, intensity_factor=intensity_factor
            )
            total_contribution += contribution

    return total_contribution


class Calculator:
    def __init__(self, x_range, y_range, z_range, propagation_factor, intensity_factor):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.propagation_factor = propagation_factor
        self.intensity_factor = intensity_factor

    def get_output(self, input_points):
        input_points_tuples = np.array(
            [(input_point.x, input_point.y, input_point.z, input_point.height) for input_point in input_points]
        )
        output_matrix = self.__initialize_output_matrix()
        output_matrix = self.__calculate_outputs(
            output_matrix=output_matrix,
            input_points=input_points_tuples,
            propagation_factor=self.propagation_factor,
            intensity_factor=self.intensity_factor,
        )

        return (
            self.__flatten_by_x(output_matrix),
            self.__flatten_by_y(output_matrix),
            self.__flatten_by_z(output_matrix),
        )

    def __initialize_output_matrix(self):
        return np.zeros((self.x_range, self.y_range, self.z_range))

    @staticmethod
    @jit(nopython=False, parallel=True)
    def __calculate_outputs(output_matrix, input_points, propagation_factor, intensity_factor):
        for x in prange(output_matrix.shape[0]):
            for y in prange(output_matrix.shape[1]):
                for z in prange(output_matrix.shape[2]):
                    output_matrix[x][y][z] = calculate_value(
                        current_point=(x, y, z),
                        input_points=input_points,
                        propagation_factor=propagation_factor,
                        intensity_factor=intensity_factor,
                    )

        return output_matrix

    @staticmethod
    @jit(nopython=False, parallel=True)
    def __flatten_by_x(matrix):
        flattened_output = []

        for _ in range(matrix.shape[0]):
            y_list = []
            for _ in range(matrix.shape[2]):
                y_list.append(0.0)
            flattened_output.append(y_list)

        for y in prange(matrix.shape[1]):
            for z in prange(matrix.shape[2]):
                flattened_value = 0.0
                for x in range(matrix.shape[0]):
                    flattened_value += matrix[x][y][z]

                flattened_output[y][z] = flattened_value

        return flattened_output

    @staticmethod
    @jit(nopython=False, parallel=True)
    def __flatten_by_y(matrix):
        flattened_output = []

        for _ in range(matrix.shape[0]):
            y_list = []
            for _ in range(matrix.shape[2]):
                y_list.append(0.0)
            flattened_output.append(y_list)

        for x in prange(matrix.shape[0]):
            for z in prange(matrix.shape[2]):
                flattened_value = 0.0
                for y in range(matrix.shape[1]):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][z] = flattened_value

        return flattened_output

    @staticmethod
    @jit(nopython=False, parallel=True)
    def __flatten_by_z(matrix):
        flattened_output = []

        for _ in range(matrix.shape[0]):
            y_list = []
            for _ in range(matrix.shape[1]):
                y_list.append(0.0)
            flattened_output.append(y_list)

        for x in prange(matrix.shape[0]):
            for y in prange(matrix.shape[1]):
                flattened_value = 0.0
                for z in range(matrix.shape[2]):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][y] = flattened_value

        return flattened_output
