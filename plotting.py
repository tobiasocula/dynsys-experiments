import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp

def basic_plot(T, X, beta, candidates):
    """
    T: timestamps
    f: actual func
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=T, y=X, name="true"))

    def xdot(t, x):
        return np.sum([c(x)*b for b,c in zip(beta,candidates)])

    sol = solve_ivp(
        xdot,
        t_span=(T[0], T[-1]),
        y0=[X[0]],
        t_eval=T,
        method='RK45'
    )

    fig.add_trace(go.Scatter(x=sol.t, y=sol.y[0], name="integrated"))
    fig.show()