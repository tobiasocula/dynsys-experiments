from main_solve import main
import numpy as np
from systems import pendulum

g = 9.81
L = 1.0
t0 = 0
x0 = [2,0] # x0, xdot_0

"""
equation:
theta" = -g/L sin(theta)
"""

candidates_sets = [
    [lambda x,y:x, lambda x,y:y, lambda x,y:x*y, lambda x,y:x**2, lambda x,y:y**2],
    [lambda x,y:x, lambda x,y:y, lambda x,y:np.sin(x), lambda x,y:np.cos(x)]
]
for cset in candidates_sets:
    beta, MSE = main(
        candidates=cset,
        t0=0,
        x0=x0,
        delta=0.5,
        num_points=10,
        system_func=pendulum,
        params={"g":g,"L":L},
        plot=False
    )

    print('beta:', beta)
    g_over_L_est = beta[2][1]
    print("g_over_L_est:", g_over_L_est, "vs real:", -g/L)
    print()


"""
python3 -m testruns.pendulum
"""