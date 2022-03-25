
import numpy as np
from numba import jit, prange

from calculation_helpers import calculate_value


class Calculator:
    def __init__(self, x_range, y_range, z_range, propagation_factor, intensity_factor):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.propagation_factor = propagation_factor
        self.intensity_factor = intensity_factor

    def get_output(self, holes):
        input_points_tuples = self.__preprocess_holes(holes)

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
    def __preprocess_holes(holes):
        input_points_processed = []
        for input_point in holes:
            for h in range(input_point.height):
                z = (input_point.z - input_point.height // 2) + h
                input_points_processed.append((input_point.x, input_point.y, z))

        return np.array(input_points_processed)

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
        flattened_output = np.zeros((matrix.shape[1], matrix.shape[2]))

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
        flattened_output = np.zeros((matrix.shape[0], matrix.shape[2]))

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
        flattened_output = np.zeros((matrix.shape[0], matrix.shape[1]))

        for x in prange(matrix.shape[0]):
            for y in prange(matrix.shape[1]):
                flattened_value = 0.0
                for z in range(matrix.shape[2]):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][y] = flattened_value

        return flattened_output
