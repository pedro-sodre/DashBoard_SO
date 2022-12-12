import os
from dash import Output, Input, html, ctx

def get_component(app):
    @app.callback(
        Output('hidden-div', 'children'),
        Input('terminal-button', 'n_clicks'))
    def openTerminal(btn1):
        if("terminal-button" == ctx.triggered_id):
            os.popen('konsole')
            #subprocess.run("gnome-terminal", shell=True, capture_output=True)
        return None
    
    return html.Div([html.Button('>_', id='terminal-button', n_clicks=0), 
                    html.Div(id='hidden-div')]                
    )