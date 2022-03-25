import time

from calculator import Calculator
from input_points_generator import HolesGenerator
from plotting_helper import PlottingHelper

X_RANGE = 200
Y_RANGE = 200
Z_RANGE = 200
HEIGHT = 50
PROPAGATION_FACTOR = 1.7
INTENSITY_FACTOR = 10000.0


if __name__ == "__main__":
    input_points = HolesGenerator.get_surface_row(
        step=20, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE, height=HEIGHT
    )
    calculator = Calculator(
        x_range=X_RANGE,
        y_range=Y_RANGE,
        z_range=Z_RANGE,
        propagation_factor=PROPAGATION_FACTOR,
        intensity_factor=INTENSITY_FACTOR,
    )

    t = time.time()

    output_x, output_y, output_z = calculator.get_output(input_points=input_points)

    print(time.time() - t)
    #
    PlottingHelper.plot_input(input_points=input_points, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE)
    PlottingHelper.plot_ouputs(output_x, output_y, output_z)
