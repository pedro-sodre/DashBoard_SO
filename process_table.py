import os
import pandas as pd


import dash
from dash import Output, Input, State, dcc, html, ctx, dash_table
import plotly.graph_objs as go
import plotly.express as px
from collections import deque


def get_process_table():
    df = pd.read_csv("process.csv", sep=';')


def command_process_csv():
    cmd = "top -b -n 3 | sed -n '7, 50{s/^ *//;s/ *$//;s/  */;/gp;};50q' >> out.csv"
    os.system(cmd)

command_process_csv()
df = pd.read_csv("process.csv", sep=';')

def get_component(app):
    return html.Div([
        html.H1('Tabela de processos'),
        dcc.Dropdown(value=10, clearable=False, style={'width': '35%'},
                     options=[10, 25, 50, 100]),
        dash_table.DataTable(
            columns=[
                {'name': 'PID', 'id': 'PID', 'type': 'numeric'},
                {'name': 'USER', 'id': 'USER', 'type': 'text'},
                {'name': 'PR', 'id': 'PR', 'type': 'numeric'},
                {'name': 'NI', 'id': 'NI', 'type': 'numeric'},
                {'name': 'VIRT', 'id': 'VIRT', 'type': 'numeric'},
                {'name': 'RES', 'id': 'RES', 'type': 'numeric'},
                {'name': 'SHR', 'id': 'SHR', 'type': 'numeric'},
                {'name': 'S', 'id': 'S', 'type': 'text'},
                {'name': '%CPU', 'id': '%CPU', 'type': 'numeric'},
                {'name': '%MEM', 'id': '%MEM', 'type': 'numeric'},
                {'name': 'TIME+', 'id': 'TIME+', 'type': 'text'},
                {'name': 'COMMAND', 'id': 'COMMAND', 'type': 'text'}
            ],
            data=df.to_dict('records'),
            filter_action='native',
            page_size=10,

            style_data={
                'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            })
    ])
