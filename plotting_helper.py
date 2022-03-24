import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
from numpy import rot90, array


class PlottingHelper:
    @staticmethod
    def plot_input(input_points, x_range, y_range, z_range):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        for input_point in input_points:
            for h in range(-input_point.height // 2, input_point.height // 2):
                ax.scatter(input_point.x, input_point.y, input_point.z + h, marker='o', color='red')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([0, x_range])
        ax.set_ylim([0, y_range])
        ax.set_zlim([0, z_range])

        plt.show()

    @staticmethod
    def plot_ouputs(output_x, output_y, output_z):
        data_x = rot90(array(output_x))
        data_y = rot90(array(output_y))
        data_z = rot90(array(output_z))

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

        max_val = max((val.max() for val in vals))

        for val, ax in zip(vals, grid):
            im = ax.imshow(val, vmin=0, vmax=max_val, cmap="hot")

        grid.cbar_axes[0].colorbar(im)

        for cax in grid.cbar_axes:
            cax.toggle_label(False)

        plt.show()
