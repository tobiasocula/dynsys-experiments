from main_solve import main
import numpy as np
from systems import lorentz_63

sigma = 1.0
rho = 0.5
beta = 0.7
t0 = 0
x0 = [-1.0, 2.0, 1.0]

beta_, MSE = main(
    candidates=[lambda t,x,y,z:1, lambda t,x,y,z:x, lambda t,x,y,z:y, lambda t,x,y,z:z, lambda t,x,y,z:x*y, lambda t,x,y,z:x**2, lambda t,x,y,z:y**2,
    lambda t,x,y,z:z**2, lambda t,x,y,z:x*z, lambda t,x,y,z:y*z],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=10,
    system_func=lorentz_63,
    params={"rho":rho,"sigma":sigma,"beta":beta},
    plot=False
)
sigma_est_one = -beta_[1][0]
sigma_est_two = beta_[2][0]
rho_est = beta_[1][1]
beta_est = -beta_[3][2]
print('sigma est one and two:', sigma_est_one, sigma_est_two, "vs real:", sigma)
print('rho est:', rho_est, 'vs real:', rho)
print('beta est:', beta_est, 'vs real:', beta)

"""
python3 -m testruns.lorentz_63
"""