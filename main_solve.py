import numpy as np
from scipy.integrate import solve_ivp
import sys

def solve(C, y):
    return np.linalg.inv(C.T @ C) @ C.T @ y

def main(candidates, t0, x0, delta, num_points, system_func, params: dict[str, int], plot=False, debug=False):
    """
    candidates: list of funcs
    
    xdot = system_func(t,x,params) with x = possibly multiple variables
    x0 can contain multiple variables

    in practice: candidates and datapoints given
    """
    T = t0 + delta * np.arange(num_points)
    X = solve_ivp(
        lambda t,x: system_func(t,x,params=params),
        t_span=(T[0], T[-1]),
        y0=x0 if isinstance(x0, list) else [x0],
        t_eval=T,
        method='RK45'
    ).y # shape (num_vars, num_datapoints)
    Xdot = np.array([system_func(t, x, params=params) for t, x in zip(T, X.T)])
    # iterating X: iterates over dimensionality, NOT datapoints -> necessary to iterate over X.T

    # design matrix
    A = np.array([
        [c(t, *x) for c in candidates]
        for t, x in zip(T, X.T)
    ]) # shape (num_points, num_candidates)

    if debug:
        print('A:'); print(A)
        print('A shape:', A.shape)

    """
    shapes: A=(numpoints, numcandidates), Xdot=X=(numpoints, dim)
    """

    beta = solve(A, Xdot)
    print('beta:', beta)
    n = A.shape[0]
    MSE = np.sum(((A @ beta) - Xdot)**2) / n
    print('MSE:', MSE)
    if plot:
        from plotting import basic_plot
        basic_plot(T, X, beta, candidates)
    return beta, MSE
        






