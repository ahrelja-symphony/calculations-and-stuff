from numba import njit
from numpy import sqrt


@njit
def calculate_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


@njit
def calculate_contribution(distance, propagation_factor, intensity_factor):
    return intensity_factor / ((1 + distance) ** propagation_factor)


@njit
def calculate_single_point_contribution(current_point, input_point, propagation_factor, intensity_factor):
    distance = calculate_distance(p1=current_point, p2=(input_point[0], input_point[1], input_point[2]))
    return calculate_contribution(distance, propagation_factor, intensity_factor)


@njit
def calculate_value(current_point, input_points, propagation_factor, intensity_factor):
    total_contribution = 0.0
    for input_point in input_points:
        total_contribution += calculate_single_point_contribution(current_point, input_point, propagation_factor, intensity_factor)

    return total_contribution



