import numpy as np

def exponential(t,x,params):
    lmbda = params["lmbda"]
    return -lmbda*x

def log_growth(t,x,params):
    r,K = params["r"],params["K"]
    return r*x*(1-x/K)

def harmonic_osc(t,x,params):
    omega = params["omega"]
    xactual, xdot = x
    return [xdot, -omega**2*xactual]

def damped_osc(t,x,params):
    c,k = params["c"], params["k"]
    xactual, xdot = x
    return [xdot, -k*xactual-c*xdot]

def pendulum(t,x,params):
    g,L = params["g"], params["L"]
    xactual, xdot = x
    return [xdot, -g/L*np.sin(xactual)]

def lotka_volterra(t,x,params):
    alpha = params["alpha"]
    beta = params["beta"]
    delta = params["delta"]
    gamma = params["gamma"]
    xactual,y = x
    return [alpha*xactual-beta*xactual*y, delta*xactual*y-gamma*y]

def van_der_pol_osc(t,x,params):
    mu = params["mu"]
    x1,x2 = x
    return [x2, mu*(1-x1**2)*x2-x1]

def duffing_osc(t,x,params):
    delta = params["delta"]
    beta = params["beta"]
    alpha = params["alpha"]
    omega = params["omega"]
    gamma = params["gamma"]
    x1,x2 = x
    return [x2, -delta*x2-alpha*x1-beta*x1**3+gamma*np.cos(omega*t)]

def lorentz_63(t,x,params):
    sigma = params["sigma"]
    rho = params["rho"]
    beta = params["beta"]
    x1,x2,x3 = x # (x,y,z)
    return [sigma*(x2-x1), x1*(rho-x3)-x2, x1*x2-beta*x3]