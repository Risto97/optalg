from optalg.test_func.base_func import Func
import numpy as np

class Sphere(Func):
    def __init__(self, bound=[-5.12, 5.12], glob_min=[0, 0, 0]):
        super().__init__(bound, glob_min)

    def func(self, x):
        z = x[0]**2 + x[1]**2
        return z


class ThCamel(Func):
    def __init__(self, bound=[-5, 5], glob_min=[0, 0, 0]):
        super().__init__(bound, glob_min)

    def func(self, x):
        return 2 * x[0]**2 - 1.05 * x[0]**4 + (x[0]**
                                               6) / 6 + x[0] * x[1] + x[1]**2


class Booth(Func):
    def __init__(self, bound=[-10, 10], glob_min=[1, 3, 0]):
        super().__init__(bound, glob_min)

    def func(self, x):
        return (x[0] + 2 * x[1] - 7)**2 + (2 * x[0] + x[1] - 5)**2


class Ackley(Func):
    def __init__(self, bound=[-32.768, 32.768], glob_min=[0, 0, 0]):
        super().__init__(bound, glob_min)

    def func(self, x):
        part_1 = -0.2 * np.sqrt(0.5 * (x[0] * x[0] + x[1] * x[1]))
        part_2 = 0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1]))
        value = np.exp(1) + 20 - 20 * np.exp(part_1) - np.exp(part_2)
        return value


class Goldstein(Func):
    def __init__(self, bound=[-2, 2], glob_min=[0, -1, 3]):
        super().__init__(bound, glob_min)

    def func(self, x):
        part1 = 1 + (
            x[0] + x[1] + 1)**2 * (19 - 14 * x[0] + 3 * x[0]**2 - 14 * x[1] +
                                   6 * x[0] * x[1] + 3 * x[1]**2)
        part2 = 30 + (2 * x[0] - 3 * x[1])**2 * (
            18 - 32 * x[0] + 12 * x[0]**2 + 48 * x[1] - 36 * x[0] * x[1] +
            27 * x[1]**2)
        return part1 * part2


class Levy(Func):
    def __init__(self, bound=[-10, 10], glob_min=[1, 1, 0]):
        super().__init__(bound, glob_min)

    def func(self, x):
        part1 = np.sin(3 * np.pi * x[0])**2 + (x[0] - 1)**2 * (
            1 + np.sin(3 * np.pi * x[1])**2)
        part2 = (x[1] - 1)**2 * (1 + np.sin(2 * np.pi * x[1])**2)
        return part1 + part2


class Shaffer(Func):
    def __init__(self, bound=[-100, 100], glob_min=[0, 0, 0]):
        super().__init__(bound, glob_min)

    def func(self, x):
        part1 = np.sin(x[0]**2 - x[1]**2)**2 - 0.5
        part2 = (1 + 0.001 * (x[0]**2 + x[1]**2))**2
        return 0.5 + part1 / part2
