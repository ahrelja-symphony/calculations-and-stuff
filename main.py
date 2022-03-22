import time
import numpy as np

import matplotlib.pyplot as plt

from calculator import Calculator
from input_points_generator import InputPointGenerator

X_RANGE = 400
Y_RANGE = 400
Z_RANGE = 400


if __name__ == "__main__":
    t = time.time()
    input_points = np.array(
        [val for val in InputPointGenerator.get_diagonal(step=5, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE)])
    calculator = Calculator(x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE)
    output = calculator.get_output(input_points=input_points)
    print(time.time() - t)
    # timeit.timeit("calculate()", setup="from __main__ import calculate", number=1)
    data = np.array(output)
    plt.imshow(data, cmap='autumn', interpolation='nearest')

    plt.title("2-D Heat Map")
    plt.show()
