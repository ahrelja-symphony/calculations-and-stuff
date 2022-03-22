import math
import numpy as np
from numpy import sqrt


class Calculator:
    def __init__(self, x_range, y_range, z_range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def get_output(self, input_points):
        output_matrix = self.__initialize_output_matrix()
        output_matrix = self.__calculate_outputs(output_matrix, input_points)
        flattened_output = self.__flatten(output_matrix)

        return flattened_output

    def __initialize_output_matrix(self):
        output_matrix = np.zeros((self.x_range, self.y_range, self.z_range))

        return output_matrix

    def __calculate_outputs(self, output_matrix, input_points):
        for x in range(self.x_range):
            for y in range(self.y_range):
                for z in range(self.z_range):
                    current_point = (x, y, z)
                    output_matrix[x][y][z] = self.__calculate_value(
                        current_point=current_point, input_points=input_points
                    )

        return output_matrix

    def __flatten(self, matrix):
        flattened_output = []

        for _ in range(self.x_range):
            y_list = []
            for _ in range(self.y_range):
                y_list.append(0)
            flattened_output.append(y_list)

        for x in range(self.x_range):
            for y in range(self.y_range):
                flattened_value = 0
                for z in range(self.z_range):
                    flattened_value += matrix[x][y][z]

                flattened_output[x][y] = flattened_value

        return flattened_output

    @staticmethod
    def __calculate_value(current_point, input_points):
        distances = []

        for input_point in input_points:
            distance = sqrt(
                (current_point[0] - input_point[0]) ** 2
                + (current_point[1] - input_point[1]) ** 2
                + (current_point[2] - input_point[2]) ** 2
            )

            distances.append(distance)

        maximum_distance = max(distances)

        return 10000 / ((1 + maximum_distance) ** 4)
