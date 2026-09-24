from main_solve import main
import numpy as np
from systems import lotka_volterra

alpha, beta, gamma, delta = 1.0, 2.0, 1.0, 0.5
t0 = 0
x0 = [2, 3]

beta_, MSE = main(
    candidates=[lambda t,x,y:1, lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x*y, lambda t,x,y:x**2, lambda t,x,y:y**2],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=10,
    system_func=lotka_volterra,
    params={"alpha":alpha,"beta":beta,"gamma":gamma,"delta":delta},
    plot=False
)

alpha_est = beta_[1][0]
beta_est = -beta_[3][0]
gamma_est = -beta_[2][1]
delta_est = beta_[3][1]
print('alpha est:', alpha_est, 'vs real:', alpha)
print('beta est:', beta_est, 'vs real:', beta)
print('gamma est:', gamma_est, 'vs real:', gamma)
print('delta est:', delta_est, 'vs real:', delta)
"""
python3 -m testruns.lotka_volterra
"""