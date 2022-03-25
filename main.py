import time

from calculator import Calculator
from input_points_generator import HolesGenerator
from plotting_helper import PlottingHelper

X_RANGE = 50
Y_RANGE = 50
Z_RANGE = 50
HEIGHT = 7
PROPAGATION_FACTOR = 1.8
INTENSITY_FACTOR = 10000


if __name__ == "__main__":
    holes = HolesGenerator.get_surface_row(
        step=5, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE, height=HEIGHT
    )
    calculator = Calculator(
        x_range=X_RANGE,
        y_range=Y_RANGE,
        z_range=Z_RANGE,
        propagation_factor=PROPAGATION_FACTOR,
        intensity_factor=INTENSITY_FACTOR,
    )

    t = time.time()

    output_x, output_y, output_z = calculator.get_output(holes=holes)

    print(time.time() - t)
    #
    PlottingHelper.plot_input(input_points=holes, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE)
    PlottingHelper.plot_ouputs(output_x, output_y, output_z)
