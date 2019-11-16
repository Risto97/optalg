import matplotlib.pyplot as plt
import logging
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging(logging_level=logging.ERROR)

from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from spice_network import connect_network, get_tree
from res_base import Res

import random
import sys
seed = random.randrange(sys.maxsize)
# seed = 420016293865968253
random.seed(seed)
print("Seed was:", seed)

res = 3.1415
res_vals = None
r = Res(set_res=res, res_vals=res_vals, max_res=8, min_res=2)
r.search(npop=100, ngen=100)
r.draw_best(fn="asd.pdf")

plist = get_tree(r)
print(plist)

figure = plt.figure(1, (10, 5))

axe = plt.subplot(111)
title = "Monte-Carlo analysis of resistor network"
axe.set_title(title)
axe.grid()

step_time = 10 @ u_ms
for i in range(100):
    circuit = Circuit(f"{i}")
    source = circuit.SinusoidalVoltageSource(
        'input', 'in1', circuit.gnd, amplitude=res @ u_V, frequency=1 @ u_Hz)
    circuit.R(1, 'in1', 'a', 0)
    circuit.R(2, circuit.gnd, 'b', 0)

    connect_network(r, circuit, tolerance=20)

    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(
        step_time=step_time, end_time=source.period * 1.5)

    res_eq = (1 @ u_uOhm)
    plot(((analysis['a']) - analysis['c']) / (res_eq))
    axe.set_ylim(-2, 2)
    axe.set_xlabel('t [s]')
    axe.set_ylabel('[V]')
    axe.legend(('Vin [V]', 'I', 'I'), loc=(.8, .8))

plt.tight_layout()
plt.show()
