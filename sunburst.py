import dash
from dash import Output, State, Input, dcc, html, ctx
import plotly.graph_objs as go
import plotly.express as px
from collections import deque
import subprocess
import pandas as pd
import os
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

fig = go.Figure(go.Sunburst(
    ids=directories['full-path'], labels=directories['directory'],
    parents=directories['parent'], values=directories['value'], hoverinfo="text", hovertext=directories['hover'], maxdepth=max_level))

app = dash.Dash()
app.layout = html.Div([
    dcc.Input(id="sunburst-root", type='text', placeholder=root),
    dcc.Input(id="sunburst-max-level", type='number',
              placeholder='3', min=2, max=recursion_level, step=1),
    html.Button('Nova raiz', id='sunburst-new-root', n_clicks=0),
    dcc.Graph(id="sun", figure=fig)
])


@app.callback(Output('sun', 'figure'), Input('sunburst-max-level', 'value'), Input('sunburst-new-root', 'n_clicks'), State('sunburst-root', 'value'), prevent_initial_call=True)
def update_graph(new_max_level, n_clicks, new_root):
    global max_level
    global directories
    change = False

    print(new_max_level)
    print(new_root)

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


app.run_server(debug=True)
