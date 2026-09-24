from main_solve import main
import numpy as np
from systems import harmonic_osc

omega = 2.5
t0 = 0
x0 = [2,0] # x0, xdot_0

"""
equation:
q" + w²q = 0
"""

beta, MSE = main(
    candidates=[lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x*y, lambda t,x,y:x**2, lambda t,x,y:y**2],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=10,
    system_func=harmonic_osc,
    params={"omega":omega},
    plot=False
)
omega_guessed = np.sqrt(-beta[0][1])
print('omega guessed:', omega_guessed, 'vs real', omega)
"""
python3 -m testruns.harm_osc
"""