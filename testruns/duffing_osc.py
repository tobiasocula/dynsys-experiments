from main_solve import main
import numpy as np
from systems import duffing_osc

alpha = 1.0
beta = 2.0
gamma = 0.5
omega = 1.0
delta = 2.0

t0 = 0
x0 = [2.0, 0.0]

beta_, MSE = main(
    candidates=[
        lambda t,x,y:1, lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x**2, lambda t,x,y:y**2, lambda t,x,y:x**3, lambda t,x,y:y**3,
    ] + [lambda t,x,y,o=o: np.cos(t*o) for o in [0.5, 0.75, 1.0, 1.25, 1.5]],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=1000,
    system_func=duffing_osc,
    params={"alpha":alpha,"beta":beta,"delta":delta,"gamma":gamma,"omega":omega},
    plot=False
)
print('beta:'); print(beta_)
alpha_est = -beta_[1][1]
beta_est = -beta_[5][1]
delta_est = -beta_[2][1]

print('alpha est:', alpha_est, 'vs real', alpha)
print('beta est:', beta_est, 'vs real', beta)
print('delta est:', delta_est, 'vs real', delta)

freqs = [0.5, 0.75, 1.0, 1.25, 1.5]
cos_coefs = beta_[7:, 1] 

abs_vals = np.abs(cos_coefs)
m = np.argmax(abs_vals)
gamma_est = cos_coefs[m]
omega_est = freqs[m]
print('gamma est:', gamma_est, 'vs real:', gamma)
print('omega est:', omega_est, 'vs real:', omega)
"""
python3 -m testruns.duffing_osc
"""