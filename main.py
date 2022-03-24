import time

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid

from calculator import Calculator
from input_points_generator import HolesGenerator

X_RANGE = 20
Y_RANGE = 20
Z_RANGE = 20

def plot_input(input_points):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for input_point in input_points:
        for h in range(-input_point.height // 2, input_point.height // 2):
            ax.scatter(input_point.x, input_point.y, input_point.z + h, marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([0, X_RANGE])
    ax.set_ylim([0, Y_RANGE])
    ax.set_zlim([0, Z_RANGE])

    plt.show()

def plot_ouputs(output_x, output_y, output_z):
    data_x = np.rot90(np.array(output_x))
    data_y = np.rot90(np.array(output_y))
    data_z = np.rot90(np.array(output_z))

    vals = [data_x, data_y, data_z]

    fig = plt.figure()

    grid = AxesGrid(fig, 111,
                    nrows_ncols=(1, 3),
                    axes_pad=0.05,
                    share_all=True,
                    label_mode="L",
                    cbar_location="right",
                    cbar_mode="single",
                    )

    for val, ax in zip(vals, grid):
        im = ax.imshow(val, vmin=0, vmax=1, cmap="hot")

    grid.cbar_axes[0].colorbar(im)

    for cax in grid.cbar_axes:
        cax.toggle_label(False)

    plt.show()


if __name__ == "__main__":
    input_points = HolesGenerator.get_surface_diagonal_cross(step=5, x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE, height=8)
    calculator = Calculator(x_range=X_RANGE, y_range=Y_RANGE, z_range=Z_RANGE)

    t = time.time()

    output_x, output_y, output_z = calculator.get_output(input_points=input_points)

    print(time.time() - t)

    plot_input(input_points)
    plot_ouputs(output_x, output_y, output_z)






