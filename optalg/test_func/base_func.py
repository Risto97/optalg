import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class Func:
    def __init__(self, bound, glob_min):
        self.f = None
        self.bound = bound
        self.glob_min = glob_min
        self.stride = 400
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.point_num = 0

    def __call__(self, x):
        return self.func(x)

    def func(self, x):
        pass

    def get_mesh(self, numpoints):
        x = np.linspace(*self.bound, numpoints)
        y = np.linspace(*self.bound, numpoints)
        X, Y = np.meshgrid(x, y)
        return X, Y

    def plot(self, text=False):
        X, Y = self.get_mesh(30)
        xy = np.stack([X, Y])
        Z = self.func(xy)

        # ax.contour3D(X, Y, Z, self.stride, cmap=cm.viridis)
        # ax.plot_surface(X, Y, Z, cmap='terrain')
        self.ax.plot_wireframe(X, Y, Z, cmap='terrain')
        self.ax.scatter(*self.glob_min, c='blue', s=30)

        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        plt.show()

    def add_point(self, point, colour='red', size=30, text=False):
        point = [*point, self.func(point)]
        self.point_num += 1
        self.ax.scatter(*point, c=colour, s=size)
        if text:
            self.ax.text(*point, f"{self.point_num}")

    def draw_points(self, plot, text=False):
        for i, point in enumerate(self.plot_points):
            plot.scatter(point[0], point[1], point[2], c=point[3], s=30)
            if text:
                plot.text(*point, f"{i}")
