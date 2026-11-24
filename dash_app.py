"""Minimal Dash app for the 84-month Macao GGR project.

Run from the project root:
    python dash_app.py
Then open http://127.0.0.1:8050

The app is a presentation layer, not a new model. It reads the cleaned panel,
refits the validation-selected 24-month model, and exposes the key results.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "gambling_visitors_cleaned.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
df["regime"] = np.where(
    df["date"] < pd.Timestamp("2020-02-01"), "pre-COVID",
    np.where(df["date"] < pd.Timestamp("2023-01-01"), "pandemic", "reopening")
)

# ---- validation-selected model (same as the notebook) --------------------
FEATURES = ["total_visitors_10k", "t"] + [f"m_{m}" for m in range(2, 13)]
TRAIN_START = pd.Timestamp("2023-03-01")
TEST_START = pd.Timestamp("2025-03-01")
train = df[(df["date"] >= TRAIN_START) & (df["date"] < TEST_START)]
model = LinearRegression().fit(train[FEATURES], train["ggr_million_mop"])

test = df[df["date"] >= TEST_START].copy()
test["pred"] = model.predict(test[FEATURES])
test_r2 = 1 - ((test["ggr_million_mop"] - test["pred"]) ** 2).sum() / (
    (test["ggr_million_mop"] - test["ggr_million_mop"].mean()) ** 2
).sum()
test_rmse = float(np.sqrt(((test["ggr_million_mop"] - test["pred"]) ** 2).mean()))
test_mae = float((test["ggr_million_mop"] - test["pred"]).abs().mean())

REGIME_ORDER = ["pre-COVID", "pandemic", "reopening"]
regime = (
    df.groupby("regime")
    .agg(months=("date", "size"), ggr_mean=("ggr_million_mop", "mean"), vis_mean=("total_visitors_10k", "mean"))
    .reindex(REGIME_ORDER)
    .reset_index()
)
regime["ggr_per_10k"] = regime["ggr_mean"] / regime["vis_mean"]

MODEL_ROWS = [
    ("M1 total arrivals", -1.169, 2369.9, 1881.2),
    ("M2 three markets", -1.322, 2451.8, 1972.1),
    ("M3 current + lag", -0.976, 2261.7, 1896.7),
    ("M4 pooled 84m", -0.609, 2040.6, 1700.7),
    ("24m validation-selected", 0.658, 941.6, 832.9),
    ("48m Model 4 (reference)", 0.666, 929.3, 755.3),
]
VALIDATION_ROWS = [
    ("18", "18", "5,656.8", "5,486.3"),
    ("24 (selected)", "24", "1,888.7", "1,496.5"),
    ("30", "30", "2,652.3", "2,228.9"),
    ("36", "36", "2,824.2", "2,483.1"),
    ("42", "42", "2,292.0", "1,953.5"),
    ("48", "48", "2,050.0", "1,749.0"),
    ("60", "60", "1,930.5", "1,619.0"),
]

COLORS = {
    "ink": "#1f2937",
    "muted": "#6b7280",
    "blue": "#1f4e79",
    "green": "#2e7d32",
    "grey": "#bfbfbf",
    "bg": "#f5f7fa",
    "card": "#ffffff",
    "line": "#e5e7eb",
}
CARD = {
    "background": COLORS["card"],
    "border": f"1px solid {COLORS['line']}",
    "borderRadius": "14px",
    "padding": "18px 20px",
    "boxShadow": "0 1px 3px rgba(0,0,0,0.04)",
}
KPI = {
    "background": COLORS["card"],
    "border": f"1px solid {COLORS['line']}",
    "borderRadius": "14px",
    "padding": "16px 18px",
    "flex": "1",
    "minWidth": "180px",
}


def overview_fig():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for label, start, end, color in [
        ("pre-COVID", "2019-01-01", "2020-01-31", "#cfe2f3"),
        ("pandemic", "2020-02-01", "2022-12-31", "#f4cccc"),
        ("reopening", "2023-01-01", "2025-12-31", "#d9ead3"),
    ]:
        fig.add_vrect(x0=start, x1=end, fillcolor=color, opacity=0.35, line_width=0)
    fig.add_trace(
        go.Scatter(x=df["date"], y=df["ggr_million_mop"], name="GGR", mode="lines",
                   line=dict(color=COLORS["blue"], width=2.4)),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df["date"], y=df["total_visitors_10k"], name="Arrivals",
                   mode="lines", line=dict(color="#c55a11", width=2.0, dash="dot")),
        secondary_y=True,
    )
    fig.update_layout(
        template="plotly_white", height=380, margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        hovermode="x unified", font=dict(family="Arial", size=12),
    )
    fig.update_yaxes(title_text="GGR (million MOP)", secondary_y=False)
    fig.update_yaxes(title_text="Arrivals (10k persons)", secondary_y=True, showgrid=False)
    return fig


def regime_fig():
    fig = go.Figure(
        go.Bar(
            x=regime["regime"], y=regime["ggr_per_10k"],
            marker_color=[COLORS["blue"], "#c55a11", COLORS["green"]],
            text=[f"{v:.1f}" for v in regime["ggr_per_10k"]], textposition="outside",
            width=0.55,
        )
    )
    fig.update_layout(
        template="plotly_white", height=330, margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="GGR per 10k arrivals (million MOP)", xaxis_title="",
        font=dict(family="Arial", size=12), yaxis=dict(range=[0, 120]),
    )
    return fig


def model_fig():
    names = [r[0] for r in MODEL_ROWS]
    colors = [COLORS["grey"]] * 4 + [COLORS["green"], COLORS["blue"]]
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Test R²", "Test RMSE (million MOP)"))
    fig.add_trace(go.Bar(x=names, y=[r[1] for r in MODEL_ROWS], marker_color=colors,
                         text=[f"{r[1]:.3f}" for r in MODEL_ROWS], textposition="outside"),
                  row=1, col=1)
    fig.add_trace(go.Bar(x=names, y=[r[2] for r in MODEL_ROWS], marker_color=colors,
                         text=[f"{r[2]:,.0f}" for r in MODEL_ROWS], textposition="outside"),
                  row=1, col=2)
    fig.update_xaxes(tickangle=-25, row=1, col=1)
    fig.update_xaxes(tickangle=-25, row=1, col=2)
    fig.update_layout(template="plotly_white", height=430, showlegend=False,
                      margin=dict(l=10, r=10, t=45, b=10), font=dict(family="Arial", size=11))
    fig.update_yaxes(range=[-1.6, 0.9], row=1, col=1)
    return fig


def pred_fig():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test["ggr_million_mop"], y=test["pred"], mode="markers+text",
                             text=test["date"].dt.strftime("%b"), textposition="top center",
                             marker=dict(size=10, color=COLORS["blue"]), name="2025 test"))
    lo = min(test["ggr_million_mop"].min(), test["pred"].min()) - 600
    hi = max(test["ggr_million_mop"].max(), test["pred"].max()) + 600
    fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", name="45° line",
                             line=dict(color="#9ca3af", dash="dash")))
    fig.update_layout(template="plotly_white", height=380, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis_title="Actual GGR (million MOP)", yaxis_title="Predicted GGR (million MOP)",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
                      font=dict(family="Arial", size=12))
    return fig


def table(headers, rows, highlight_row=None):
    trs = []
    for i, row in enumerate(rows):
        is_hi = highlight_row is not None and i == highlight_row
        trs.append(html.Tr([
            html.Td(str(v), style={
                "padding": "8px 10px", "borderBottom": f"1px solid {COLORS['line']}",
                "fontWeight": "700" if is_hi else "400",
                "background": "#e8f5e9" if is_hi else "transparent",
                "textAlign": "left" if j == 0 else "center",
            }) for j, v in enumerate(row)
        ]))
    return html.Table([
        html.Thead(html.Tr([
            html.Th(h, style={"padding": "8px 10px", "textAlign": "left" if j == 0 else "center",
                              "fontSize": "12px", "color": COLORS["muted"],
                              "borderBottom": f"2px solid {COLORS['line']}"})
            for j, h in enumerate(headers)
        ])),
        html.Tbody(trs),
    ], style={"width": "100%", "borderCollapse": "collapse", "fontSize": "13px"})


app = Dash(__name__, title="Macao GGR 84m")
server = app.server

app.layout = html.Div(
    style={"background": COLORS["bg"], "minHeight": "100vh", "fontFamily": "Arial, sans-serif",
           "color": COLORS["ink"], "padding": "0 0 32px 0"},
    children=[
        html.Div([
            html.Div("Macao GGR & Inbound Visitors", style={"fontSize": "13px", "letterSpacing": "1.5px",
                                                             "textTransform": "uppercase", "opacity": 0.8}),
            html.H1("84 months, three regimes, one validation-selected model",
                    style={"margin": "6px 0 4px 0", "fontSize": "28px"}),
            html.Div("CISC7204 Assignment 02 · Huang Yudan · Chen Yuhan",
                     style={"fontSize": "13px", "opacity": 0.85}),
        ], style={"background": COLORS["blue"], "color": "white", "padding": "26px 34px 22px 34px"}),

        html.Div([
            html.Div([html.Div("84", style={"fontSize": "28px", "fontWeight": "700"}),
                      html.Div("monthly observations", style={"color": COLORS["muted"], "fontSize": "12px"})], style=KPI),
            html.Div([html.Div("3", style={"fontSize": "28px", "fontWeight": "700"}),
                      html.Div("regimes: pre-COVID / pandemic / reopening", style={"color": COLORS["muted"], "fontSize": "12px"})], style=KPI),
            html.Div([html.Div(f"{test_r2:.3f}", style={"fontSize": "28px", "fontWeight": "700", "color": COLORS["green"]}),
                      html.Div("2025 test R² (24m model)", style={"color": COLORS["muted"], "fontSize": "12px"})], style=KPI),
            html.Div([html.Div("1,888.7", style={"fontSize": "28px", "fontWeight": "700"}),
                      html.Div("2024 validation RMSE", style={"color": COLORS["muted"], "fontSize": "12px"})], style=KPI),
        ], style={"display": "flex", "gap": "14px", "padding": "18px 34px 0 34px", "flexWrap": "wrap"}),

        html.Div([
            dcc.Tabs([
                dcc.Tab(label="Overview", children=[
                    html.Div([html.Div("84-month panel with regime shading",
                                       style={"fontWeight": "700", "marginBottom": "6px"}),
                              html.Div("GGR collapses in 2020, recovers in 2023, then flattens. The same slope cannot describe all three.",
                                       style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "8px"}),
                              dcc.Graph(figure=overview_fig(), config={"displayModeBar": False})], style=CARD)
                ]),
                dcc.Tab(label="Regimes", children=[
                    html.Div([
                        html.Div("GGR per 10,000 arrivals", style={"fontWeight": "700", "marginBottom": "6px"}),
                        html.Div("Pre-COVID 74.4 · pandemic 101.7 · reopening 63.7. A single visitor slope is not identified across regimes.",
                                 style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "8px"}),
                        dcc.Graph(figure=regime_fig(), config={"displayModeBar": False}),
                    ], style=CARD),
                ]),
                dcc.Tab(label="Models", children=[
                    html.Div([
                        html.Div("Pooled models fail; the 24m model is validation-selected",
                                 style={"fontWeight": "700", "marginBottom": "6px"}),
                        html.Div("2025-03..2025-12 test window, same for every model. Green = 24m validation-selected; blue = 48m reference.",
                                 style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "8px"}),
                        dcc.Graph(figure=model_fig(), config={"displayModeBar": False}),
                        html.Div("2024 validation: 24m has the lowest RMSE (1,888.7), narrowly ahead of 60m (1,930.5).",
                                 style={"fontSize": "12px", "color": COLORS["muted"]}),
                    ], style=CARD),
                ]),
                dcc.Tab(label="Validation", children=[
                    html.Div([
                        html.Div("Window selected on 2024 only — 2025 untouched",
                                 style={"fontWeight": "700", "marginBottom": "6px"}),
                        html.Div("Training ends before 2024; validation is 2024-01..2024-12. Lower RMSE is better.",
                                 style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "8px"}),
                        table(["Window (months)", "Train months", "Validation RMSE", "Validation MAE"],
                              VALIDATION_ROWS, highlight_row=1),
                    ], style=CARD),
                ]),
                dcc.Tab(label="2025 test", children=[
                    html.Div([
                        html.Div("Predicted vs actual, 2025-03..2025-12",
                                 style={"fontWeight": "700", "marginBottom": "6px"}),
                        html.Div(f"Test R² = {test_r2:.3f} · RMSE = {test_rmse:,.1f} · MAE = {test_mae:,.1f} million MOP.",
                                 style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "8px"}),
                        dcc.Graph(figure=pred_fig(), config={"displayModeBar": False}),
                    ], style=CARD),
                ]),
                dcc.Tab(label="What-if", children=[
                    html.Div([
                        html.Div("Illustrative what-if (not a forecast)",
                                 style={"fontWeight": "700", "marginBottom": "6px"}),
                        html.Div("Set arrivals and a calendar month; the app applies the 24m model with the month index fixed at the chosen value.",
                                 style={"color": COLORS["muted"], "fontSize": "13px", "marginBottom": "12px"}),
                        html.Div([
                            html.Div([html.Label("Arrivals (10k persons)"),
                                      dcc.Slider(id="vis", min=150, max=450, step=10, value=350,
                                                 marks={150: "150", 250: "250", 350: "350", 450: "450"})],
                                     style={"marginBottom": "26px"}),
                            html.Div([html.Label("Calendar month"),
                                      dcc.Dropdown(id="month", options=[{"label": f"Month {m}", "value": m} for m in range(1, 13)],
                                                   value=10, clearable=False)],
                                     style={"marginBottom": "18px"}),
                            html.Div([html.Label("Month index (t)"),
                                      dcc.Slider(id="t", min=75, max=96, step=1, value=75,
                                                 marks={75: "75", 84: "84", 96: "96"})]),
                        ], style={"maxWidth": "620px"}),
                        html.Div(id="pred-out", style={"marginTop": "22px", "fontSize": "26px", "fontWeight": "700",
                                                       "color": COLORS["green"]}),
                        html.Div("Illustrative only: the model is a first draft and does not include supply-side controls.",
                                 style={"marginTop": "8px", "fontSize": "12px", "color": COLORS["muted"]}),
                    ], style=CARD),
                ]),
            ], style={"margin": "18px 34px 0 34px"})
        ]),
    ],
)


@app.callback(Output("pred-out", "children"), [Input("vis", "value"), Input("month", "value"), Input("t", "value")])
def update_prediction(vis, month, t):
    row = {f: 0.0 for f in FEATURES}
    row["total_visitors_10k"] = float(vis)
    row["t"] = float(t)
    if month != 1:
        row[f"m_{month}"] = 1.0
    pred = float(model.predict(pd.DataFrame([row], columns=FEATURES))[0])
    return f"Predicted GGR: {pred:,.0f} million MOP"


if __name__ == "__main__":
    app.run(debug=False, port=8050)
