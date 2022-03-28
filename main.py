import time
import numpy as np
from calculator import Calculator, calculate_value, calculate_distance
from input_points_generator import HolesGenerator
from plotting_helper import PlottingHelper

X_RANGE = 200
Y_RANGE = 200
Z_RANGE = 200
HEIGHT = 10
PROPAGATION_FACTOR = 1.8
INTENSITY_FACTOR = 10000.0


if __name__ == "__main__":
    holes = np.array(
        HolesGenerator.get_surface_row(step=5, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE, height=HEIGHT)
    )
    calculator = Calculator(
        x_range=X_RANGE,
        y_range=Y_RANGE,
        z_range=Z_RANGE,
        propagation_factor=PROPAGATION_FACTOR,
        intensity_factor=INTENSITY_FACTOR,
    )




    print("Matrix size: " + str(X_RANGE * Y_RANGE * Z_RANGE))
    print("Number of holes: " + str(len(holes)))
    print("Height" + str(HEIGHT))

    start_time = time.time()

    output_x, output_y, output_z = calculator.get_output(holes=holes)

    print(f"Running time: {str(time.time() - start_time)}")

    # PlottingHelper.plot_input(input_points=holes, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE)
    # PlottingHelper.plot_ouputs(output_x, output_y, output_z)
