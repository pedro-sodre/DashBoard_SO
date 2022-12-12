import pandas as pd
import subprocess

from dash import Output, Input, dcc, html, dash_table


def get_process_data():
    command_data = subprocess.run(
        "top -b -n 1 | sed -n '7, 50{s/^ *//;s/ *$//;s/  */;/gp;};50q'", shell=True, capture_output=True).stdout.decode().strip()

    columns = command_data.split("\n")[0].split(";")
    rows = command_data[command_data.index("\n") + 1:]

    return pd.DataFrame([row.split(";") for row in rows.split('\n')], columns=columns)


def get_component(app):
    @app.callback(Output('process-table', 'data'), [Input('graph-update', 'n_intervals')])
    def update_table(n_intervals):
        return get_process_data().to_dict('records')

    @app.callback(Output('process-table', 'page_size'), [Input('page-size-dropdown', 'value')])
    def update_table(value):
        return value

    return html.Div([
        html.H1('Tabela de processos'),
        dcc.Dropdown(id='page-size-dropdown', value=10, clearable=False, style={'width': '35%'},
                     options=[10, 25, 50, 100]),
        dash_table.DataTable(id='process-table',
                             columns=[
                                 {'name': 'PID', 'id': 'PID', 'type': 'numeric'},
                                 {'name': 'User', 'id': 'USER', 'type': 'text'},
                                 {'name': 'Priority', 'id': 'PR',
                                  'type': 'numeric'},
                                 {'name': 'Nice Value', 'id': 'NI',
                                  'type': 'numeric'},
                                 {'name': 'Total Virtual Memory',
                                  'id': 'VIRT', 'type': 'numeric'},
                                 {'name': 'Total physical memory (kB)',
                                  'id': 'RES', 'type': 'numeric'},
                                 {'name': 'Total shared memory (kB)',
                                  'id': 'SHR', 'type': 'numeric'},
                                 {'name': 'S', 'id': 'S', 'type': 'text'},
                                 {'name': 'CPU Usage (%)', 'id': '%CPU',
                                  'type': 'numeric'},
                                 {'name': 'Memory Usage (%)',
                                  'id': '%MEM', 'type': 'numeric'},
                                 {'name': 'CPU Time usage',
                                  'id': 'TIME+', 'type': 'text'},
                                 {'name': 'COMMAND', 'id': 'COMMAND', 'type': 'text'}
                             ],
                            #  filter_action='native',
                            #  sort_action='native',
                             data=get_process_data().to_dict('records'),
                             style_data={
                                 'overflow': 'hidden',
                                 'textOverflow': 'ellipsis',
                             })
    ])
