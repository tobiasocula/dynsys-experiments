from main_solve import main, main_2
import numpy as np
from scipy.integrate import solve_ivp
from systems import duffing_osc

paramnames = ["alpha","beta","gamma","delta","omega"]


def run_1(params, T_length, dts, init_conditions):
    """
    different time interval, initial conditions
    """


    num_conds = len(init_conditions)
    num_dts = len(dts)
    # 5 = number of params
    error_matrix = np.zeros((num_conds, num_dts, 5))
    rel_error_matrix = np.zeros((num_conds, num_dts, 5))
    mses = np.zeros((num_conds, num_dts))

    alpha,beta,gamma,delta,omega = [params[p] for p in paramnames]

    for i,d in enumerate(dts):
        for j,x0 in enumerate(init_conditions):

            num_points = int(T_length/d)
            T = d * np.arange(num_points)
            
            X = solve_ivp(
                lambda t,x: duffing_osc(t,x,params=params),
                t_span=(T[0], T[-1]),
                y0=x0 if isinstance(x0, list) else [x0],
                t_eval=T,
                method='RK45'
            ).y # shape (num_vars, num_datapoints)

            beta_, MSE = main_2(
                    candidates=[lambda t,x,y:1, lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x**2, lambda t,x,y:y**2, lambda t,x,y:x**3, lambda t,x,y:y**3
                ] + [lambda t,x,y,o=o: np.cos(t*o) for o in [0.5, 0.75, 1.0, 1.25, 1.5]],
                X=X,
                T=T,
                params=params,
            )

            mses[j,i] = MSE

            alpha_est = -beta_[1][1]
            beta_est = -beta_[5][1]
            delta_est = -beta_[2][1]

            freqs = [0.5, 0.75, 1.0, 1.25, 1.5]
            cos_coefs = beta_[7:, 1]

            abs_vals = np.abs(cos_coefs)
            m = np.argmax(abs_vals)
            gamma_est = cos_coefs[m]
            omega_est = freqs[m]

            error_matrix[j, i,:] = [
                alpha - alpha_est,
                beta - beta_est,
                gamma - gamma_est,
                delta - delta_est,
                omega - omega_est
            ]
            rel_error_matrix[j, i,:] = [
                (alpha - alpha_est) / alpha,
                (beta - beta_est) / beta,
                (gamma - gamma_est) / gamma,
                (delta - delta_est) / delta,
                (omega - omega_est) / omega
            ]

    return error_matrix, rel_error_matrix, mses

def run_2(params, x0, T_length, dts, sigmas):
    """
    different time intervals and noise levels
    sigmas: list of lists: inner list is of form (std_variable_1, std_variable_2, ...)
    """

    num_dts = len(dts)
    num_sigmas = len(sigmas)
    # 5 = number of params
    error_matrix = np.zeros((num_dts, num_sigmas, 5))
    rel_error_matrix = np.zeros((num_dts, num_sigmas, 5))
    mses = np.zeros((num_dts, num_sigmas))

    alpha,beta,gamma,delta,omega = [params[p] for p in paramnames]

    for i,d in enumerate(dts):
        num_points = int(T_length/d)
        T = d * np.arange(num_points)
        X = solve_ivp(
            lambda t,x: duffing_osc(t,x,params=params),
            t_span=(T[0], T[-1]),
            y0=x0 if isinstance(x0, list) else [x0],
            t_eval=T,
            method='RK45'
        ).y # shape (num_vars, num_datapoints)
        for j,sigma in enumerate(sigmas):
            X_noise = X.copy()
            for k in range(X.shape[0]): # over vars
                noise = np.random.normal(0, sigma[k], size=X.shape[1])
                X_noise[k,:] += noise

            beta_, MSE = main_2(
                    candidates=[lambda t,x,y:1, lambda t,x,y:x, lambda t,x,y:y, lambda t,x,y:x**2, lambda t,x,y:y**2, lambda t,x,y:x**3, lambda t,x,y:y**3
                ] + [lambda t,x,y,o=o: np.cos(t*o) for o in [0.5, 0.75, 1.0, 1.25, 1.5]],
                X=X_noise,
                T=T,
                params=params,
            )

            mses[i,j] = MSE

            alpha_est = -beta_[1][1]
            beta_est = -beta_[5][1]
            delta_est = -beta_[2][1]

            freqs = [0.5, 0.75, 1.0, 1.25, 1.5]
            cos_coefs = beta_[7:, 1]

            abs_vals = np.abs(cos_coefs)
            m = np.argmax(abs_vals)
            gamma_est = cos_coefs[m]
            omega_est = freqs[m]

            error_matrix[i,j,:] = [
                alpha - alpha_est,
                beta - beta_est,
                gamma - gamma_est,
                delta - delta_est,
                omega - omega_est
            ]
            rel_error_matrix[i,j,:] = [
                (alpha - alpha_est) / alpha,
                (beta - beta_est) / beta,
                (gamma - gamma_est) / gamma,
                (delta - delta_est) / delta,
                (omega - omega_est) / omega
            ]

    return error_matrix, rel_error_matrix, mses
            

