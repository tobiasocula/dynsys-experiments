import plotly.graph_objects as go
import plotly.colors as pc
from plotly.subplots import make_subplots
import numpy as np
from duffingOscTesting.run_duffing import run_2
import sys

"""
python3 -m duffingOscTesting.with_noise
"""

paramnames = ["alpha","beta","gamma","delta","omega"]
colors = pc.qualitative.Plotly

x0 = [1.0, 0.0]

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

alpha = 1.0
beta = 2.0
gamma = 0.5
omega = 1.0
delta = 2.0

T_length = 40

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

sigmas = [
    [0.01, 0.01],
    [0.1, 0.05],
    [0.1, 0.01],
    [0.5, 0.01],
    [0.5, 0.2],
    [1.0, 0.5],
    [1.0, 0.01]
]

error_matrix, rel_error_matrix, mses = run_2(params, x0, T_length, dts, sigmas)


num_deltas = len(dts)
params = {p:eval(p) for p in paramnames}
specs = [[{"secondary_y": True} for _ in range(3)] for _ in range(2)]  # 2 rows x 3 cols

fig = make_subplots(rows=2, cols=3, specs=specs, subplot_titles=paramnames + ["mse"])

box = to_box(2, 3)


for i, sigma in enumerate(sigmas):
    color = colors[i % len(colors)]
    for j, paramname in enumerate(paramnames):
        r, c = box[j][0] + 1, box[j][1] + 1

        fig.add_trace(go.Scatter(
            x=dts,
            y=error_matrix[:, i, j],
            name=f"param: {paramname} - sigma: {sigma}",
            line=dict(color=color)
        ), row=r, col=c, secondary_y=False)

        fig.add_trace(go.Scatter(
            x=dts,
            y=rel_error_matrix[:, i, j],
            name=f"param: {paramname} - sigma: {sigma}",
            line=dict(color=color, dash="dash")
        ), row=r, col=c, secondary_y=True)

    fig.add_trace(go.Scatter(
        x=dts,
        y=mses[:, i],
        name=f"mses - sigma: {sigma}",
        line=dict(color=color)
    ), row=2, col=3, secondary_y=False)

# Axis titles: also need secondary_y= to target left vs right
for j, paramname in enumerate(paramnames):
    r, c = box[j][0] + 1, box[j][1] + 1
    fig.update_xaxes(title_text="dt", row=r, col=c)
    fig.update_yaxes(title_text="error", row=r, col=c, secondary_y=False)
    fig.update_yaxes(title_text="rel. error", row=r, col=c, secondary_y=True)

fig.show()