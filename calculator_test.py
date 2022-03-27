import numpy as np
from snapshottest import TestCase

from calculator import Calculator
from input_points_generator import HolesGenerator


class CalculatorTest(TestCase):
    def test_calculator(self):
        X_RANGE = 20
        Y_RANGE = 20
        Z_RANGE = 20
        HEIGHT = 5
        PROPAGATION_FACTOR = 1.8
        INTENSITY_FACTOR = 10000.0

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

        output_x, output_y, output_z = calculator.get_output(holes=holes)

        self.assertMatchSnapshot(output_x.__repr__())
        self.assertMatchSnapshot(output_y.__repr__())
        self.assertMatchSnapshot(output_z.__repr__())
