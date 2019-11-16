import deap.gp as gp
from PySpice.Unit import *
import random


def get_tree(r):
    def writeback(plist, node, num=None):
        if isinstance(node, gp.Primitive):
            val = f"{node.name}{num}"
        elif isinstance(node, gp.Terminal):
            val = node.value

        cnt = len(plist)
        while (cnt > 0):
            if plist[cnt - 1][1][0] is None:
                plist[cnt - 1][1][0] = val
                return
            elif plist[cnt - 1][1][1] is None:
                plist[cnt - 1][1][1] = val
                return

            cnt -= 1

    plist = []
    cnt = 0
    for node in r.best:
        if node.arity == 2:
            p = [f"{node.name}{cnt}", [None, None]]
            if cnt > 0:
                writeback(plist, node, cnt)
            plist.append(p)
            cnt += 1
        elif node.arity == 0:
            writeback(plist, node)

    return plist


def connect_network(r, circuit, tolerance=0):
    def gen_mc_res(value, tolerance=tolerance):
        if tolerance == 0:
            return value
        else:
            return value + (value *
                            (random.uniform(-tolerance, tolerance) / 100))

    def gen_rnum(start=0):
        rnum = start
        while True:
            yield rnum
            rnum += 1

    plist = get_tree(r)
    rnum = gen_rnum(start=3)

    full_nets = []
    cnt = 0
    for i, node in enumerate(plist):
        if not isinstance(node[1][0], str) and not isinstance(node[1][1], str):
            if node[0][0] == 'P':
                circuit.R(
                    next(rnum), f'{i}1', f'{i}2',
                    gen_mc_res(float(node[1][0]), tolerance))
                circuit.R(next(rnum), f'{i}1', f'{i}2', node[1][1])
            elif node[0][0] == 'S':
                circuit.R(
                    next(rnum), f'{i}1', f'{i}3',
                    gen_mc_res(float(node[1][0]), tolerance))
                circuit.R(next(rnum), f'{i}3', f'{i}2', node[1][1])

            full_nets.append(node[0])

    def get_halfnode(node):
        ret_val, ret_str = 0, ""
        for val in node[1]:
            if isinstance(val, float):
                ret_val = val
            if isinstance(val, str):
                ret_str = val[0:]
        return ret_val, ret_str

    while full_nets is not []:
        for i, node in enumerate(plist):
            nodes_are_str = isinstance(node[1][0], str) and isinstance(
                node[1][1], str)
            full_node = nodes_are_str and node[1][0] in full_nets and node[1][
                1] in full_nets
            half_node = (isinstance(node[1][0],float) and node[1][1] in full_nets) or \
                (isinstance(node[1][1],float) and node[1][0] in full_nets)
            if full_node:
                if node[0][0] == 'P':
                    circuit.R(
                        next(rnum), f'{node[1][0][1:]}1', f'{node[1][1][1:]}1',
                        0)
                    circuit.R(
                        next(rnum), f'{node[1][0][1:]}2', f'{node[1][1][1:]}2',
                        0)
                    circuit.R(
                        next(rnum), f'{node[0][1:]}1', f'{node[1][1][1:]}1', 0)
                    circuit.R(
                        next(rnum), f'{node[0][1:]}2', f'{node[1][1][1:]}2', 0)
                elif node[0][0] == 'S':
                    circuit.R(next(rnum), f'{i}1', f'{node[1][0][1:]}1', 0)
                    circuit.R(next(rnum), f'{i}2', f'{node[1][1][1:]}2', 0)
                    circuit.R(
                        next(rnum), f'{node[1][0][1:]}2', f'{node[1][1][1:]}1',
                        0)

                full_nets.remove(node[1][0])
                full_nets.remove(node[1][1])
                full_nets.append(node[0])

            elif half_node:
                val, ind = get_halfnode(node)
                if node[0][0] == 'P':
                    circuit.R(
                        next(rnum), f'{node[0][1:]}1', f'{node[0][1:]}2',
                        gen_mc_res(val, tolerance))
                    circuit.R(next(rnum), f'{node[0][1:]}1', f'{ind[1:]}1', 0)
                    circuit.R(next(rnum), f'{node[0][1:]}2', f'{ind[1:]}2', 0)
                    full_nets.remove(ind)
                elif node[0][0] == 'S':
                    circuit.R(
                        next(rnum), f'{node[0][1:]}1', f'{node[0][1:]}3', gen_mc_res(val, tolerance))
                    circuit.R(next(rnum), f'{node[0][1:]}3', f'{ind[1:]}1', 0)
                    circuit.R(next(rnum), f'{ind[1:]}2', f'{node[0][1:]}2', 0)
                    full_nets.remove(ind)

                full_nets.append(node[0])

        if full_nets[0] == 'P0' or full_nets[0] == 'S0':
            if isinstance(plist[0][1][1], float):
                gnd_point = "0"
            else:
                gnd_point = plist[0][1][1][1:]
            circuit.R(next(rnum), 'a', 'c', 1@u_uOhm)
            circuit.R(next(rnum), 'c', '01', 0)
            circuit.R(next(rnum), 'b', f'{gnd_point}2', 0)
            break
