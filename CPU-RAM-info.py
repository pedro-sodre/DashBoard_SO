import os
import platform
import subprocess
import re
import psutil
import subprocess
from math import ceil

import dash
from dash import Output, Input, State, dcc, html, ctx
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

recursion_level = 4
max_level = 3
root = subprocess.check_output("echo ~", shell=True).decode().strip()

command = f"du -bd {recursion_level} {root}"
command_data = subprocess.run(
    command, shell=True, capture_output=True).stdout.decode().strip()
directories = pd.DataFrame(
    columns=['full-path', 'directory', 'parent', 'value', 'hover'])

for dir in command_data.split('\n'):
    dir_data = dir.split("\t")
    dir_size = int(dir_data[0])
    hover = None
    if dir_size > 1e12:
        hover = f"{round(dir_size/1e12, 2)}TB"
    elif dir_size > 1e9:
        hover = f"{round(dir_size/1e9, 2)}GB"
    elif dir_size > 1e6:
        hover = f"{round(dir_size/1e6, 2)}MB"
    elif dir_size > 1e3:
        hover = f"{round(dir_size/1e3, 2)}KB"
    else:
        hover = f"{dir_size}B"
    full_path = dir_data[1]
    index_last_slash = full_path.rindex("/")
    name = full_path[index_last_slash + 1:]
    parent = None
    if (full_path != root):
        parent = full_path[:index_last_slash]
    directories.loc[len(directories)] = (
        full_path, name, parent, dir_size, hover)


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
        dcc.Graph(id='cpu-usage', animate=True),
    ]),
    html.Div([
    dcc.Input(id="sunburst-root", type='text', placeholder=root),
    dcc.Input(id="sunburst-max-level", type='number',
              placeholder='3', min=2, max=recursion_level, step=1),
    html.Button('Nova raiz', id='sunburst-new-root', n_clicks=0),
    dcc.Graph(id="sun", figure= go.Figure(go.Sunburst(
    ids=directories['full-path'], labels=directories['directory'],
    parents=directories['parent'], values=directories['value'], hoverinfo="text", hovertext=directories['hover'], maxdepth=max_level)))
    ])
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

    add_cpu_usage_to_dataframe(cpu_usage, cpu_time)

    total = px.line(cpu_usage[cpu_usage.cpu.isin(cpus)], x="time", y="usage", color="cpu", range_x=[
                    min(cpu_usage["time"]), max(cpu_usage["time"])])
    return total

@app.callback(Output('sun', 'figure'), Input('sunburst-max-level', 'value'), Input('sunburst-new-root', 'n_clicks'), State('sunburst-root', 'value'), prevent_initial_call=True)
def update_graph(new_max_level, n_clicks, new_root):
    global max_level
    global directories
    change = False

    if ctx.triggered_id == 'sunburst-max-level' and new_max_level != None and new_max_level > 0 and new_max_level <= recursion_level:
        max_level = new_max_level
        change = True

    if ctx.triggered_id == 'sunburst-new-root' and new_root != None and os.path.isdir(new_root):
        command = f"du -bd {recursion_level} {root}"
        command_data = subprocess.run(
            command, shell=True, capture_output=True).stdout.decode().strip()
        directories = pd.DataFrame(
            columns=['full-path', 'directory', 'parent', 'value', 'hover'])

        for dir in command_data.split('\n'):
            dir_data = dir.split("\t")
            dir_size = int(dir_data[0])
            hover = None
            if dir_size > 1e12:
                hover = f"{round(dir_size/1e12, 2)}TB"
            elif dir_size > 1e9:
                hover = f"{round(dir_size/1e9, 2)}GB"
            elif dir_size > 1e6:
                hover = f"{round(dir_size/1e6, 2)}MB"
            elif dir_size > 1e3:
                hover = f"{round(dir_size/1e3, 2)}KB"
            else:
                hover = f"{dir_size}B"
            full_path = dir_data[1]
            index_last_slash = full_path.rindex("/")
            name = full_path[index_last_slash + 1:]
            parent = None
            if (full_path != root):
                parent = full_path[:index_last_slash]
            directories.loc[len(directories)] = (
                full_path, name, parent, dir_size, hover)
        change = True
    if change:
        return go.Figure(go.Sunburst(ids=directories['full-path'], labels=directories['directory'], parents=directories['parent'], values=directories['value'], hoverinfo="text", hovertext=directories['hover'], maxdepth=max_level, ))


@app.callback(Output('sunburst-root', 'value'), Input('sun', 'clickData'), prevent_initial_call=True)
def update_graph(clickData):
    global root
    if clickData != None:
        new_root = clickData["points"][0]["id"]
        if new_root != root:
            root = new_root
        else:
            root = new_root[:new_root.rindex("/")]
        return root

if __name__ == "__main__":
    app.run_server(debug=True)
