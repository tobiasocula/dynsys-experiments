import plotly.graph_objects as go
import plotly.colors as pc
from plotly.subplots import make_subplots
import numpy as np
from duffingOscTesting.run_duffing import run_1
import sys

def to_box(vertical, horizontal):
    res = []
    v,h = 0,0
    res.append([v,h])
    while True:
        if h == horizontal - 1:
            if v == vertical - 1:
                return res
            h = 0
            v += 1
        else:
            h += 1
        res.append([v,h])


"""
python3 -m duffingOscTesting.different_dts_inits

one plot for: mses, alpha, beta, gamma, delta, omega
for each plot: different lines for different initial conditions
"""

paramnames = ["alpha","beta","gamma","delta","omega"]
colors = pc.qualitative.Plotly

init_conditions = [
    [2.0, 0.0],
     [3.0, 0.0],
     [0.0, 1.0],
     [0.0, 2.0],
     [1.0, 1.0],
     [2.0, 2.0]
]

alpha = 1.0
beta = 2.0
gamma = 0.5
omega = 1.0
delta = 2.0

T_length = 20

t0 = 0
deltas_start = 0.05
deltas_end = 1.5
deltas_step = 0.1
 
dts = np.arange(
    deltas_start,
    deltas_end + 0.5 * deltas_step,
    deltas_step
)

num_deltas = len(dts)
params = {p:eval(p) for p in paramnames}

error_matrix, rel_error_matrix, mses = run_1(params, T_length, dts, init_conditions)

specs = [[{"secondary_y": True} for _ in range(3)] for _ in range(2)]  # 2 rows x 3 cols
fig = make_subplots(rows=2, cols=3, subplot_titles=paramnames + ["mse"], specs=specs)
box = to_box(2, 3)

for i, x0 in enumerate(init_conditions):
    color = colors[i % len(colors)]
    for j, paramname in enumerate(paramnames):
        r, c = box[j][0] + 1, box[j][1] + 1

        fig.update_xaxes(title_text="dt", row=r, col=c)
        fig.update_yaxes(title_text="error", row=r, col=c, secondary_y=False)
        fig.update_yaxes(title_text="rel. error", row=r, col=c, secondary_y=True)

        fig.add_trace(go.Scatter(
            x=dts,
            y=error_matrix[i, :, j],
            name=f"param: {paramname} - init condition: {x0}",
            line=dict(color=color)
        ), row=r, col=c, secondary_y=False)

        fig.add_trace(go.Scatter(
            x=dts,
            y=rel_error_matrix[i, :, j],
            name=f"param: {paramname} - init condition: {x0}",
            line=dict(color=color, dash="dash")
        ), row=r, col=c, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=dts,
        y=mses[i, :],
        name=f"mses - init condition: {x0}",
        line=dict(color=color)
    ), row=2, col=3, secondary_y=False)

fig.show()


