from optalg.test_func.functions import *
import random as rnd


def hill_climbing(f, numiter, eps):
    x = rnd.uniform(*f.bound)
    y = rnd.uniform(*f.bound)
    current = f([x, y])
    print("Start position: ", x, y, f([x, y]))
    curr_x, curr_y = x, y
    f.add_point([x, y], colour='green', size=60)
    for i in range(numiter):
        x = x + rnd.choice([eps, -eps])
        y = y + rnd.choice([eps, -eps])
        candidate = f([x, y])
        if candidate <= current:
            current = candidate
            curr_x, curr_y = x, y

        if (i % (numiter/50)) == 0:  # Add black path
            f.add_point([curr_x, curr_y], colour='black', size=10)

    return curr_x, curr_y


f = Shaffer()
x, y = hill_climbing(f, 1000000, 0.1)
f.add_point([x, y], colour='red', text=True, size=60)
print("Final Position: ", x, y, f([x, y]))
print("Global Minimum: ", *f.glob_min)
f.plot()
