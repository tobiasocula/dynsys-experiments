from main_solve import main
import numpy as np
from systems import exponential

lmbda = .5
t0 = 0
x0 = 2

main(
    candidates=[lambda t,x, n=n: x**n for n in range(4)],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=10,
    system_func=exponential,
    params={"lmbda":lmbda},
    plot=True
)
"""
python3 -m testruns.basic_exponential
"""