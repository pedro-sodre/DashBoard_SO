import platform

from dash import html

import psutil

from dash import Output, Input, html

import multiOS

import other_hardware

def get_component(app):

    @app.callback(Output('battery', 'children'), [Input('graph-update', 'n_intervals')])
    def update_table(n_intervals):
        dados = psutil.sensors_battery()
        if dados == None:
            return ""
        return f"percentagem de bateria: {round(dados.percent, 2)}% {'(carregando)' if dados.power_plugged else ''}"

    return html.Div([
        html.H3(f"SO: {platform.system()}    //  processador: {multiOS.get_processor_name()} //  Tipo do processador: {platform.machine()}    //  Nome de rede: {platform.node()}"),
        html.H3(f"GPU: {other_hardware.get_gpu()}, Placa-mãe: {other_hardware.get_motherboard()} "),
        
        html.H3(f'Usuário: {other_hardware.get_user_name()}  // PID Login: {other_hardware.get_user_pid()}'),
        html.H3(id="battery")
    ])
