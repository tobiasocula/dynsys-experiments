from main_solve import main
import numpy as np
from systems import log_growth

r = 0.5
K = 3
t0 = 0
x0 = 1
beta, MSE = main(
    candidates=[lambda t,x, n=n: x**n for n in range(4)],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=10,
    system_func=log_growth,
    params={"r":r,"K":K},
    plot=False
)

r_guessed = beta[1]
K_guessed = -beta[1]/beta[2]
print('r_guessed:', r_guessed, 'vs r_true:', r)
print('K_guessed:', K_guessed, 'vs K_true:', K)

"""
python3 -m testruns.log_growth
"""