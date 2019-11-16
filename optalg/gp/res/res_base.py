import operator
import pygraphviz as pgv
import random
from deap import base, creator, gp, tools, algorithms
import numpy
from si_prefix import si_format
import math


class Res:
    def __init__(self,
                 set_res,
                 res_series='E24',
                 min_res=1,
                 max_res=8,
                 res_vals=None):

        self.set_res = set_res
        self.res_series = res_series
        self.res_vals = []
        self.max_res = max_res
        self.tree_depth = math.ceil(math.log2(self.max_res))
        self.min_depth = math.floor(math.log2(min_res))

        self.pop = []
        self.hof = []
        self.best = 0

        if res_vals is None:
            self.res_vals = []
            self.gen_res_vals()
        else:
            self.res_vals = res_vals

        self.pset = gp.PrimitiveSet("MAIN", 0)
        self.pset.addPrimitive(self.P, 2)
        self.pset.addPrimitive(self.S, 2)
        for val in self.res_vals:
            self.pset.addTerminal(val)

        creator.create("Fitness", base.Fitness, weights=(-1.0, ))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.Fitness)

        self.tb = base.Toolbox()
        self.tb.register(
            "expr",
            gp.genHalfAndHalf,
            pset=self.pset,
            min_=self.min_depth,
            max_=self.tree_depth)
        self.tb.register("individual", tools.initIterate, creator.Individual,
                         self.tb.expr)
        self.tb.register("population", tools.initRepeat, list,
                         self.tb.individual)
        self.tb.register("compile", gp.compile, pset=self.pset)

        self.tb.register("evaluate", self.evaluate)
        self.tb.register("select", tools.selTournament, tournsize=3)
        self.tb.register("mate", gp.cxOnePoint)
        self.tb.register(
            "expr_mut",
            gp.genFull,
            min_=self.min_depth,
            max_=self.tree_depth)
        self.tb.register(
            "mutate", gp.mutUniform, expr=self.tb.expr_mut, pset=self.pset)

        self.tb.decorate(
            "mate",
            gp.staticLimit(
                key=operator.attrgetter("height"), max_value=self.tree_depth))
        self.tb.decorate(
            "mutate",
            gp.staticLimit(
                key=operator.attrgetter("height"), max_value=self.tree_depth))

    def S(self, r1, r2):
        return r1 + r2

    def P(self, r1, r2):
        return (r1 * r2) / (r1 + r2)

    def gen_res_vals(self):
        res_base_vals = []
        if self.res_series == "E24":
            res_base_vals = [
                1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
            ]

            self.res_vals = [
                round(base_val * 10**i, 2) for i in range(7)
                for base_val in res_base_vals
            ]

        return self.res_vals

    def evaluate(self, individual):
        func = self.tb.compile(expr=individual)
        return (abs(func - self.set_res), )

    def search(self, npop=100, ngen=100, cxpb=0.7, mutpb=0.2, verbose=False):
        lambda_ = npop

        self.pop = self.tb.population(n=npop)
        self.hof = tools.HallOfFame(10)

        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        mstats.register("avg", numpy.mean)
        mstats.register("std", numpy.std)
        mstats.register("min", numpy.min)
        mstats.register("max", numpy.max)

        self.pop, log = algorithms.eaMuPlusLambda(
            self.pop,
            self.tb,
            mu=npop,
            lambda_=lambda_,
            cxpb=cxpb,
            mutpb=mutpb,
            ngen=ngen,
            stats=mstats,
            halloffame=self.hof,
            verbose=verbose)
        self.best = self.hof[0]
        self.print_ind(self.best)

        return self.pop, log, self.hof

    def print_ind(self, ind):
        res_val = self.tb.compile(expr=self.best)
        rel_err = (res_val - self.set_res) * 100 / res_val
        print(f"Target___value: {self.set_res}")
        print(f"Evolved__value: {res_val}")
        print(f"Relative_error: {str(round(rel_err,7))}%")

    def rel_error(self, ind):
        res_val = self.tb.compile(expr=self.best)
        rel_err = (res_val - self.set_res) * 100 / res_val
        return rel_err

    def draw_best(self, fn="tree.pdf"):
        self.draw_ind(self.best, fn)

    def draw_ind(self, ind, fn="tree.pdf"):
        res_val = self.tb.compile(expr=self.best)
        rel_err = (res_val - self.set_res) * 100 / res_val
        nodes, edges, labels = gp.graph(self.best)
        g = pgv.AGraph(strict=False, overlap=False, splines=True, nodesep='.5')
        g.node_attr['shape'] = 'box'
        g.add_node(f'Target: {self.set_res}\nActual: {res_val}\nError: {str(round(rel_err,7))}%')
        g.node_attr['shape'] = 'ellipse'
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="dot")

        for i in nodes:
            n = g.get_node(i)
            if labels[i] != 'S' and labels[i] != 'P':
                labels[i] = si_format(float(labels[i]), precision=1)
            n.attr["label"] = labels[i]

        g.draw(fn)
