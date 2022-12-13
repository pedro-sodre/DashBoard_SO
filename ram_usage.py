import psutil

from collections import deque
from math import ceil
import plotly.graph_objs as go
from dash import Output, Input, dcc, html
import plotly.graph_objs as go


def get_used_ram():
    return psutil.virtual_memory().used / (1000000000)


def get_total_ram():
    return psutil.virtual_memory().total / (1000000000)


time_ram = deque(maxlen=30)
used_ram = deque(maxlen=30)
time_ram.append(1)
used_ram.append(get_used_ram())


def _update_graph():
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


def get_component(app):
    @app.callback(Output('ram-usage', 'figure'), [Input('ram-update', 'n_intervals')])
    def update_graph(n_intervals):
        return _update_graph()

    return html.Div([
        dcc.Interval(
            id='ram-update',
            interval=1000,
            max_intervals=-1,
            n_intervals=0
        ),
        html.H1(
            f'Utilização de RAM em Gigabytes - Total instalado é {round(get_total_ram(), 2)}GB'),
        dcc.Graph(id='ram-usage', animate=True)])
