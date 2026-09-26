import numpy as np
from scipy.integrate import solve_ivp
import sys

def solve(C, y, thresh=None):
    return np.linalg.lstsq(C, y, rcond=None)[0]
    
def slts_solve(C, y, thresh, max_iters=20):
    Cused = C.copy()
    finished = False
    # C: shape (n,p) = (num_observations, num_candidate_functions)
    # y: shape (n,m) = (num_observations, num_system_equations)
    # output: shape (p,m) = (num_candidate_functions, num_system_equations)
    iters = 0
    coefs = None
    p,m = Cused.shape[1],y.shape[1]
    while not finished and iters <= max_iters:
        coefs = solve(Cused, y, thresh)
        old_coefs = coefs.copy()
        mask = np.abs(coefs) >= thresh # (p,m)
        for k in range(mask.shape[1]):
            coefs_new = solve(Cused[:,mask[:,k]], y[:,k], thresh) # (something, 1)
            coefs[:,k] = 0
            coefs[mask[:,k],k] = coefs_new
        iters += 1
        finished = np.array_equal(old_coefs, coefs)

    return coefs


def main(candidates, t0, x0, delta, num_points, system_func, params: dict[str, int], debug=False, thresh=0.01):
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
    print('shape xdot:', Xdot.shape)

    # design matrix
    A = np.array([
        [c(t, *x) for c in candidates]
        for t, x in zip(T, X.T)
    ]) # shape (num_points, num_candidates)

    print('Xdot and A shapes:', Xdot.shape, A.shape) # (2, 100) (100, 12)

    if debug:
        print('A:'); print(A)
        print('A shape:', A.shape)

    """
    shapes: A=(numpoints, numcandidates), Xdot=X=(numpoints, dim)
    """

    #beta = solve(A, Xdot)
    beta = slts_solve(A, Xdot, thresh)
    print('beta shape:', beta.shape)
    print('beta:', beta)
    n = A.shape[0]
    MSE = np.sum(((A @ beta) - Xdot)**2) / n
    return beta, MSE

def main_2(candidates, X, T, params, debug=False, thresh=0.01):
    """
    not using the exact system_function but np.gradient
    """
    delta = T[1]-T[0]
    # T: shape (n)
    # X: shape (m,n) (m = number of equations in system)
    Xdot = np.gradient(X, delta, axis=1).T
    
    # design matrix
    A = np.array([
        [c(t, *x) for c in candidates]
        for t, x in zip(T, X.T)
    ]) # shape (num_points, num_candidates)

    print('Xdot and A shapes:', Xdot.shape, A.shape) # (10, 2) (10, 12)

    beta = slts_solve(A, Xdot, thresh)

    n = A.shape[0]
    MSE = np.sum(((A @ beta) - Xdot)**2) / n
    return beta, MSE






