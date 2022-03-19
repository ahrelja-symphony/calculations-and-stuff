import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from memory_profiler import profile

X_RANGE = 100
Y_RANGE = 100
Z_RANGE = 100

NUMBER_OF_INPUT_POINTS = 5


def initialize_output_matrix():
    output_matrix = []

    for _ in range(X_RANGE):
        x_array = []
        for _ in range(Y_RANGE):
            y_array = []
            for _ in range(Z_RANGE):
                y_array.append(0)
            x_array.append(y_array)
        output_matrix.append(x_array)

    return output_matrix


@profile
def calculate_outputs(output_matrix, input_points):
    sqrt = math.sqrt
    for x in range(X_RANGE):
        for y in range(Y_RANGE):
            for z in range(Z_RANGE):
                current_point = (x, y, z)
                output_matrix[x][y][z] = calculate_value(current_point=current_point, input_points=input_points, sqrt=sqrt)

    return output_matrix


def calculate_value(current_point, input_points, sqrt):
    distances = []

    for input_point in input_points:
        distance = sqrt(
            (current_point[0] - input_point[0]) ** 2
            + (current_point[1] - input_point[1]) ** 2
            + (current_point[2] - input_point[2]) ** 2
        )

        distances.append(distance)

    maximum_distance = max(distances)

    return 1 / (1 + maximum_distance)

def flatten(matrix):
    flattened_output = []

    for _ in range(X_RANGE):
        y_list = []
        for _ in range(Y_RANGE):
            y_list.append(0)
        flattened_output.append(y_list)

    for x in range(X_RANGE):
        for y in range(Y_RANGE):
            flattened_value = 0
            for z in range(Z_RANGE):
                flattened_value += matrix[x][y][z]

            flattened_output[x][y] = flattened_value

    # for z in range(Z_RANGE):
    #     for y in range(Y_RANGE):
    #         flattened_value = 0
    #         for x in range(X_RANGE):
    #             flattened_value += matrix[x][y][z]
    #
    #         flattened_output[z][y] = flattened_value


    return flattened_output

if __name__ == "__main__":
    output_matrix = initialize_output_matrix()
    input_points = [
        (random.randint(0, X_RANGE), random.randint(0, Y_RANGE), random.randint(0, Z_RANGE))
        for _ in range(NUMBER_OF_INPUT_POINTS)
    ]
    output_matrix = calculate_outputs(output_matrix=output_matrix, input_points=input_points)
    flattened_matrix = flatten(matrix=output_matrix)

    print(flattened_matrix)

    data = np.array(flattened_matrix)
    plt.imshow(data, cmap='autumn', interpolation='nearest')

    plt.title("2-D Heat Map")
    plt.show()

    # print(output_matrix)
