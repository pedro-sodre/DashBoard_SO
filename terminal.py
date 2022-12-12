import psutil
import os
import subprocess
import pandas as pd
from dash import Output, Input, dcc, html, ctx
import plotly.express as px

def get_component(app):
    @app.callback(
        Output('hidden-div', 'children'),
        Input('terminal-button', 'n_clicks'))
    def openTerminal(btn1):
        if("terminal-button" == ctx.triggered_id):
            #os.popen('gnome-terminal')
            #print("button clicked")
            subprocess.run("gnome-terminal", shell=True, capture_output=True)
            return html.Div("Button clicked")
        return None
    
    return html.Div([html.Button('>_', id='terminal-button', n_clicks=0), 
                    html.Div(id='hidden-div')]                
    )#,    html.Div(id='hidden-div', style={'display':'none'})