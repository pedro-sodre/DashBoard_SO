import psutil

import pandas as pd
from dash import Output, Input, dcc, html, ctx
import plotly.express as px


def get_cpu_usage():
    return psutil.cpu_percent(interval=0)


def get_per_cpu_usage():
    return psutil.cpu_percent(interval=0, percpu=True)


def add_cpu_usage_to_dataframe(df, time):
    index = 0
    if len(df.index) > 0:
        index = max(df.index + 1)
    df.loc[index] = [time, "total", get_cpu_usage()]
    index += 1
    per_cpu_usage = get_per_cpu_usage()
    for x in range(0, n_cpus):
        df.loc[index] = [time, f"cpu {x}", per_cpu_usage[x]]
        index += 1


n_cpus = len(get_per_cpu_usage())
cpu_options = [f"cpu {x}" for x in range(0, n_cpus)]
cpu_options.append("total")

cpu_time = 0
cpu_usage = pd.DataFrame(columns=["time", "cpu", "usage"])

add_cpu_usage_to_dataframe(cpu_usage, 0)


def _update_graph(cpus):
    global time_cpu
    global cpu_usage
    global cpu_time

    cpu_time = cpu_time + 1

    # removes medidas com idade maior que a máxima pra não vazar memória
    cpu_usage.drop(cpu_usage[cpu_usage["time"] < (
        cpu_time - 30)].index, inplace=True)

    add_cpu_usage_to_dataframe(cpu_usage, cpu_time)

    return px.line(cpu_usage[cpu_usage.cpu.isin(cpus)], x="time", y="usage", color="cpu", range_x=[
        min(cpu_usage["time"]), max(cpu_usage["time"])])


def get_component(app):
    @app.callback(Output('cpu-usage', 'figure'), [Input('cpu-update', 'n_intervals'), Input('cpu-checklist', 'value')])
    def update_graph(n_intervals, cpus):
        return _update_graph(cpus)

    return html.Div([
            dcc.Interval(
        id='cpu-update',
        interval=1000,  
        max_intervals=-1,
        n_intervals=0
    ),
        html.H1('Utilização dos processadores (%)'),
        dcc.Checklist(id="cpu-checklist",
                      options=cpu_options, value=cpu_options),
        dcc.Graph(id='cpu-usage', animate=True)
    ])
