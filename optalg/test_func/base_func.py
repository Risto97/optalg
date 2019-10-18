import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class Func:
    def __init__(self, bound, glob_min):
        self.f = None
        self.bound = bound
        self.glob_min = glob_min
        self.plot_points = []
        self.stride = 400

    def __call__(self, x):
        return self.func(x)

    def func(self, x):
        pass

    def get_mesh(self, numpoints):
        x = np.linspace(*self.bound, numpoints)
        y = np.linspace(*self.bound, numpoints)
        X, Y = np.meshgrid(x, y)
        return X, Y

    def plot(self):
        X, Y = self.get_mesh(30)
        xy = np.stack([X, Y])
        Z = self.func(xy)

        fig = plt.figure()
        ax = plt.axes(projection='3d')
        # ax.contour3D(X, Y, Z, self.stride, cmap=cm.viridis)
        ax.plot_wireframe(X, Y, Z, cmap='terrain')
        # ax.plot_surface(X, Y, Z, cmap='terrain')
        ax.scatter(*self.glob_min, c='blue', s=30)
        self.draw_points(ax)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.show()

    def add_point(self, point):
        point = [*point, self.func(point)]
        self.plot_points.append(point)

    def draw_points(self, plot):
        for i, point in enumerate(self.plot_points):
            plot.scatter(*point, c='red', s=30)
            plot.text(*point, f"{i}")
