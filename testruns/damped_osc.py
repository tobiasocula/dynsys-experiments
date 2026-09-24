from main_solve import main
import numpy as np
from systems import damped_osc

c = 1.0
k = 1.0
t0 = 0
x0 = [2,0] # x0, xdot_0

"""
equation:
q" + cq' + kq = 0
"""

beta, MSE = main(
    candidates=[lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x*y, lambda t,x,y:x**2, lambda t,x,y:y**2],
    t0=0,
    x0=x0,
    delta=0.5,
    num_points=10,
    system_func=damped_osc,
    params={"k":k,"c":c},
    plot=False,
)
k_guessed = -beta[0][1]
c_guessed = -beta[1][1]
print('k guessed:', k_guessed, 'vs real', k)
print('c guessed:', c_guessed, 'vs real', c)
"""
python3 -m testruns.damped_osc
"""