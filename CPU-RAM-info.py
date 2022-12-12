import platform

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

import ram_usage
import cpu_usage
import disc_usage
import process_table
import static_info

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dcc.Interval(
        id='graph-update',  # ativa o update do gráfico
        interval=1000,  # tempo de delay para cada update
        max_intervals=-1,
        n_intervals=0
    ),
    static_info.get_component(app),
    dbc.Row([
        dbc.Col(disc_usage.get_component(app), width=5),
        dbc.Col(ram_usage.get_component(app), width=7),
    ]),
    cpu_usage.get_component(app),
    process_table.get_component(app)
])


if __name__ == "__main__":
    app.run_server(debug=True)
