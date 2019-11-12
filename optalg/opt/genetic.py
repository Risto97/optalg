from optalg.test_func.functions import *
import random as rnd
import numpy as np

# def breed(par1, par2):
#     val1 = (par1[0] + par2[0]) / 2
#     val2 = (par1[1] + par2[1]) / 2
#     return [val1, val2]


def saturate(x, f):
    for i in range(len(x)):
        if x[i] > f.bound[1]:
            x[i] = f.bound[1]
        if x[i] < f.bound[0]:
            x[i] = f.bound[0]
    return x


def breed(par1, par2, f):
    child1, child2 = [], []
    for i in range(2):
        val1 = par1[i] % 0.1
        val2 = par2[i] % 0.1
        child1.append((par1[i] - val1) + val2)
        child2.append((par2[i] - val2) + val1)

    child1 = saturate(child1, f)
    child2 = saturate(child2, f)
    return child1, child2


def get_fitness(pop):
    fitness = [(f(val), i) for i, val in enumerate(pop)]
    fitness.sort()
    fitness, perm = zip(*fitness)
    fitness = list(fitness)
    return fitness, perm


def sort_pop(pop, perm):
    pop = [pop[i] for i in perm]
    return pop


def round_pop_to_fmt(pop, fmt):
    return [[fmt(p[0]).__float__(), fmt(p[1]).__float__()] for p in pop]


def gen(f, init_pop=10, fmt=Fixp[8, 16]):
    pop = [[rnd.uniform(*f.bound),
            rnd.uniform(*f.bound)] for i in range(init_pop)]

    for i in range(10000):
        fitness, perm = get_fitness(pop)
        pop = sort_pop(pop, perm)

        # variance = np.var(fitness)
        variance = np.var(pop)
        # print(fitness)
        # print("Variance: ", variance)
        # print(pop)
        if variance < 100000:
            for i in range(2):
                pop[rnd.randint((init_pop - 1) // 2, init_pop - 1)] = [
                    rnd.uniform(*f.bound),
                    rnd.uniform(*f.bound)
                ]
        cand_pop = []
        cand_fitness = []
        for i in range(2):
            p1, p2 = breed(pop[i], pop[i + 1], f)
            cand_pop.append(p1)
            cand_pop.append(p2)
        cand_fitness, cand_perm = get_fitness(cand_pop)
        cand_pop = sort_pop(cand_pop, cand_perm)
        pop[-1] = cand_pop[-1]
        pop[-2] = cand_pop[-2]

    return pop[0]


# f = Booth()
f = Shaffer()
x, y = gen(f, fmt=fmt)

f.add_point([x, y], colour='red', text=True, size=60)
print("Final Position: ", x, y, f([x, y]))
print("Global Minimum: ", *f.glob_min)
f.plot()
