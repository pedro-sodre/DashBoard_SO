import platform

from dash import html

import psutil

from dash import Output, Input, html

import multiOS


def get_component(app):

    @app.callback(Output('battery', 'children'), [Input('graph-update', 'n_intervals')])
    def update_table(n_intervals):
        dados = psutil.sensors_battery()
        return f"percentagem de bateria: {round(dados.percent, 2)}% {'(carregando)' if dados.power_plugged else ''}"

    return html.Div([
        html.H3(f"SO: {platform.system()}   processador: {multiOS.get_processor_name()} Tipo da máquina: {platform.machine()}   Nome de rede: {platform.node()}"),
        html.H3(id="battery")
    ])
