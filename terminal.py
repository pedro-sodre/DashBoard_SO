import os
from dash import Output, Input, html, ctx
import subprocess


def get_component(app):
    @app.callback(
        Output('hidden-div', 'children'),
        Input('terminal-button', 'n_clicks'))
    def openTerminal(btn1):
        if ("terminal-button" == ctx.triggered_id):
            try:
                os.popen('konsole')
            except:
                subprocess.run("gnome-terminal", shell=True,
                               capture_output=True)

        return None

    return html.Div([html.Button('>_', id='terminal-button', n_clicks=0),
                    html.Div(id='hidden-div')])
