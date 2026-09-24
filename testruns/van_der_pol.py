from main_solve import main
import numpy as np
from systems import van_der_pol_osc

mu = 0.3
t0 = 0
x0 = [2.0, 0.0]

beta, MSE = main(
    candidates=[
        lambda t,x,y:1, lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x*y, lambda t,x,y:x**2, lambda t,x,y:y**2, lambda t,x,y:x*y,
        lambda t,x,y: x**2*y, lambda t,x,y:x*y**2, lambda t,x,y:x**3, lambda t,x,y:y**3
    ],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=100,
    system_func=van_der_pol_osc,
    params={"mu":mu},
    plot=False
)
print('beta:', beta)
mu_guessed_1 = beta[2][1]
mu_guessed_2 = -beta[7][1]
print('mu guessed 1:', mu_guessed_1, "and mu guessed 2", mu_guessed_2, 'vs real mu:', mu)
"""
python3 -m testruns.van_der_pol
"""