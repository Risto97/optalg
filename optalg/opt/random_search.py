from optalg.test_func.functions import *
import random as rnd

def random_search(f, numiter):
    x = rnd.uniform(*f.bound)
    y = rnd.uniform(*f.bound)
    best_x, best_y = x, y
    best = f([x, y])
    print("Start Position: ", x, y, f([x, y]))
    for i in range(numiter):
        x = rnd.uniform(*f.bound)
        y = rnd.uniform(*f.bound)
        candidate = f([x,y])

        if candidate < best:
            best = candidate
            best_x, best_y = x, y

        if (i % 100000) == 0:
            f.add_point([best_x,best_y])
            print(i)

    return best_x, best_y

f = Ackley()
x,y = random_search(f, 1000000)
f.add_point([x,y])
print("Final Position: ", x, y, f([x, y]))
print("Global Minimum: ", *f.glob_min)
f.plot()
