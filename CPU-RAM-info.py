import platform

import dash
from dash import dcc, html

from multiOS import *
import ram_usage
import cpu_usage
import disc_usage
import process_table

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Interval(
        id='graph-update',  # ativa o update do gráfico
        interval=1000,  # tempo de delay para cada update
        max_intervals=-1,
        n_intervals=0
    ),
    html.H1(f"SO: {platform.system()}   processador: {get_processor_name()}"),
    ram_usage.get_component(app),
    cpu_usage.get_component(app),
    disc_usage.get_component(app),
    process_table.get_component(app)
])


if __name__ == "__main__":
    app.run_server(debug=True)
