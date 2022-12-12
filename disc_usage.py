import platform
import subprocess
import os
from multiOS import get_slash, get_home_path

from dash import Output, Input, State, dcc, html, ctx
import plotly.graph_objs as go

import pandas as pd

max_depth = 4
max_level = 3
root = get_home_path()
directories = pd.DataFrame()


def make_disc_df(new_root, new_max_depth):
    global root
    global max_depth

    root = new_root
    max_depth = new_max_depth

    if platform.system() == "Windows":
        command = f"du -l {max_depth} {root}"
    elif platform.system() == "Linux":
        command = f"du -bd {max_depth} {root}"

    command_data = subprocess.run(
        command, shell=True, capture_output=True).stdout.decode().strip()

    directories = pd.DataFrame(
        columns=['full-path', 'directory', 'parent', 'value', 'hover'])

    for dir in command_data.split('\n'):
        dir_data = dir.split("\t")
        try:
            dir_size = int(dir_data[0].replace(".", ""))
        except:
            continue

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
        index_last_slash = full_path.rindex(get_slash())
        name = full_path[index_last_slash + 1:]
        parent = None
        if (full_path != root):
            parent = full_path[:index_last_slash]
        directories.loc[len(directories)] = (
            full_path, name, parent, dir_size, hover)
    return directories


directories = make_disc_df(root, max_depth)


def make_disc_fig(max_level, data):
    return go.Figure(go.Sunburst(
        ids=data['full-path'], labels=data['directory'],
        parents=data['parent'], values=data['value'], hoverinfo="text",
        hovertext=data['hover'], maxdepth=max_level))


def _update_graph(new_max_level, new_root):
    global max_level
    global directories
    change = False

    if ctx.triggered_id == 'sunburst-max-level' and new_max_level != None and new_max_level > 0 and new_max_level <= max_depth:
        max_level = new_max_level
        change = True

    if ctx.triggered_id == 'sunburst-new-root' and new_root != None and os.path.isdir(new_root):
        change = True
        directories = make_disc_df(new_root, max_depth)
    if change:
        return make_disc_fig(max_level, directories)


def _update_root_text(clickData):
    global root
    if clickData != None:
        new_root = clickData["points"][0]["id"]
        if new_root != root:
            root = new_root
        else:
            root = new_root[:new_root.rindex(get_slash())]
        return root


def get_component(app):
    @app.callback(Output('sun', 'figure'), Input('sunburst-max-level', 'value'), Input('sunburst-new-root', 'n_clicks'), State('sunburst-root', 'value'), prevent_initial_call=True)
    def update_graph(new_max_level, n_clicks, new_root):
        return _update_graph(new_max_level, new_root)

    @app.callback(Output('sunburst-root', 'value'), Input('sun', 'clickData'), prevent_initial_call=True)
    def update_root_text(clickData):
        return _update_root_text(clickData)

    return html.Div([
        html.H1('Utilização de disco'),
        dcc.Input(id="sunburst-root", type='text', placeholder=root),
        dcc.Input(id="sunburst-max-level", type='number',
                  placeholder=max_level, min=2, max=max_depth, step=1),
        html.Button('Nova raiz', id='sunburst-new-root', n_clicks=0),
        dcc.Graph(id="sun", figure=make_disc_fig(max_level, directories))
    ])
