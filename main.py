import time

from calculator import Calculator
from calculator1 import Calculator as CalculatorV1
from calculator2 import Calculator as CalculatorV2
from calculator3 import Calculator as CalculatorV3
from input_points_generator import HolesGenerator
from plotting_helper import PlottingHelper
import argparse

HEIGHT = 10
PROPAGATION_FACTOR = 1.8
INTENSITY_FACTOR = 10000

CALCULATOR_IMPLEMENTATIONS = {
    0: Calculator,
    1: CalculatorV1,
    2: CalculatorV2,
    3: CalculatorV3,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fictional calc.")
    parser.add_argument("samples", metavar="N", type=int, nargs="+", help="an integer for the accumulator")
    parser.add_argument("--version", type=int, default=0)
    parser.add_argument("--intensity", default=INTENSITY_FACTOR)
    parser.add_argument("--propagation", default=PROPAGATION_FACTOR)
    parser.add_argument("--show-plot", default=False, action="store_true")
    parser.add_argument("--height", default=HEIGHT)

    args = parser.parse_args()

    height = args.height
    intensity = args.intensity
    propagation = args.propagation
    CalculatorImpl = CALCULATOR_IMPLEMENTATIONS[args.version]

    for n in args.samples:
        x_range = y_range = z_range = n

        # Prep
        # holes = HolesGenerator.get_surface_row(
        #     step=5, x_range=x_range, y_range=y_range, z_range=z_range, height=height
        # )
        holes = HolesGenerator.get_surface_row(5, x_range=x_range, y_range=y_range, z_range=z_range, height=HEIGHT)
        # holes = HolesGenerator.get_diagonal(
        #     step=5, x_range=x_range, y_range=y_range, z_range=z_range, height=height
        # )
        calculator = CalculatorImpl(
            x_range=x_range,
            y_range=y_range,
            z_range=z_range,
            propagation_factor=propagation,
            intensity_factor=intensity,
        )

        # Calculation
        ts = time.time()
        output_x, output_y, output_z = calculator.get_output(holes=holes)
        te = time.time()
        print(f"Execution time for N = {n} => {te - ts}")
        print(f"Number of holes: {len(holes)}")

        # Visuals
        # PlottingHelper.plot_input(f"input_n_{n}",
        #                           input_points=holes,
        #                           x_range=x_range,
        #                           y_range=y_range,
        #                           z_range=z_range,
        #                           show=args.show_plot)
        # PlottingHelper.plot_outputs(f"output_n_{n}",
        #                             output_x,
        #                             output_y,
        #                             output_z,
        #                             show=args.show_plot)
