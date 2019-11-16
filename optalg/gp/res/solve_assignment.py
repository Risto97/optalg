from res_base import Res
import math

res_vals = [1.]
## E24
rel_error = 100
pi_error = 0.031847134
r = Res(set_res=math.pi, res_vals=None, max_res=8)
while abs(rel_error) > pi_error:
    r.search(npop=100, ngen=100)
    rel_error = r.rel_error(r.best)
    print("")
r.draw_best(fn="e24_pi.pdf")
print("Found E24 pi")

rel_error = 100
while abs(rel_error) > pi_error:
    r.set_res = math.e
    r.search(npop=100, ngen=100)
    rel_error = r.rel_error(r.best)
    print("")
r.draw_best(fn="e24_e.pdf")
print("Found E24 e")

rel_error = 100
while abs(rel_error) > pi_error:
    r.set_res = math.sqrt(2)
    r.search(npop=100, ngen=100)
    rel_error = r.rel_error(r.best)
    print("")
r.draw_best(fn="e24_sqrt2.pdf")
print("Found E24 sqrt(2)")

## 1R resistor
rel_error = 100
res_vals = [1.]
r = Res(set_res=math.pi, res_vals=res_vals, max_res=16)
while abs(rel_error) > pi_error:
    r.search(npop=100, ngen=100)
    rel_error = r.rel_error(r.best)
    print("")
r.draw_best(fn="r1_pi.pdf")
print("Found 1R pi")

e_error = pi_error*3
rel_error = 100
res_vals = [1.]
while abs(rel_error) > e_error:
    r.set_res = math.e
    r.search(npop=100, ngen=100)
    rel_error = r.rel_error(r.best)
    print("")
r.draw_best(fn="r1_e.pdf")
print("Found 1R e")

rel_error = 100
res_vals = [1.]
while abs(rel_error) > e_error:
    r.set_res = math.sqrt(2)
    r.search(npop=100, ngen=100)
    rel_error = r.rel_error(r.best)
    print("")
r.draw_best(fn="r1_sqrt2.pdf")
print("Found 1R sqrt(2)")
