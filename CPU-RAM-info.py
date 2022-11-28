import os
import platform
import subprocess
import re
import psutil
import time
import subprocess
from math import ceil

import dash
from dash import Output, Input, dcc, html
import plotly.graph_objs as go
import plotly.express as px
from collections import deque

import pandas as pd

# Pega o nome do processador (dependendo do sistema operacional é diferente)
def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

def get_used_ram():
    return psutil.virtual_memory().used / (1000000000)


def get_total_ram():
    return psutil.virtual_memory().total / (1000000000)


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


time_ram = deque(maxlen=30)
used_ram = deque(maxlen=30)
time_ram = [1]
used_ram = [get_used_ram()]

n_cpus = len(get_per_cpu_usage())

cpu_options = [f"cpu {x}" for x in range(0, n_cpus)]
cpu_options.append("total")

cpu_time = 0
cpu_usage = pd.DataFrame(columns=["time", "cpu", "usage"])

add_cpu_usage_to_dataframe(cpu_usage, 0)

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Interval(
        id='graph-update',  # ativa o update do gráfico
        interval=1000,  # tempo de delay para cada update
        max_intervals=-1,
        n_intervals=0
    ),
    html.H1(f"SO: {platform.system()}   processador: {get_processor_name()}"),
    html.Div([html.H1(f'Utilização de RAM em Gigabytes - Total instalado é {round(get_total_ram(), 2)}GB'),
        dcc.Graph(id='ram-usage', animate=True)]),
    html.Div([
         html.H1('Utilização dos processadores (%)'),
        dcc.Checklist(id="cpu-checklist",
                      options=cpu_options, value=cpu_options),
        dcc.Graph(id='cpu-usage', animate=True)
    ]),
])


@app.callback(Output('ram-usage', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph(n_intervals):
    global time_ram
    global used_ram
    global total_ram
    time_ram.append(time_ram[-1] + 1)
    used_ram.append(get_used_ram())

    used = go.Scatter(
        x=list(time_ram),
        y=list(used_ram),
        mode='lines+markers',
    )
    return {
        'data': [used],
        'layout': go.Layout(
            xaxis=dict(range=[min(time_ram), max(time_ram)]),
            yaxis=dict(range=[0, ceil(get_total_ram())]),
        )
    }


@app.callback(Output('cpu-usage', 'figure'), [
    Input('graph-update', 'n_intervals'),
    Input('cpu-checklist', 'value')
])
def update_graph(n_intervals, cpus):
    global time_cpu
    global cpu_usage
    global cpu_time

    cpu_time = cpu_time + 1

    #removes medidas com idade maior que a máxima pra não vazar memória
    cpu_usage.drop(cpu_usage[cpu_usage["time"] < (cpu_time - 30)].index, inplace=True)
    print(cpu_usage)

    add_cpu_usage_to_dataframe(cpu_usage, cpu_time)

    total = px.line(cpu_usage[cpu_usage.cpu.isin(cpus)], x="time", y="usage", color="cpu", range_x=[
                    min(cpu_usage["time"]), max(cpu_usage["time"])])
    return total


if __name__ == "__main__":
    app.run_server(debug=True)
