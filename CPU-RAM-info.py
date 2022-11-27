import os, platform, subprocess, re
import psutil
import time
import subprocess


import dash
from dash import Output, Input, dcc, html
import plotly
import random
import plotly.graph_objs as go
from collections import deque 


#Cria um X e um Y com o máximo de iterações (para limitar o gráfico iterativo)
X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

app = dash.Dash(__name__)
app.layout = html.Div([dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id = 'graph-update', #ativa o update do gráfico
            interval = 1000 #tempo de delay para cada update
        )
    ]
)

#desenha o gráfico
@app.callback(Output('live-graph', 'figure'), event=[Input('graph-update', 'interval')])

#atualiza o gráfico, nesse caso o X é atualizado de 1 em 1, e o Y é atualizado com algum número randômico
def update_graph():
    global X
    global Y
    X.append(X[-1]+1)
    Y.append(Y[-1]+(Y[-1]*random.uniform(-0.1, 0.1)))

    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
         )
    return {'data':[data], 'layout': go.Layout(xaxis = dict(range=[min(X), max(X)]), yaxis = dict(range=[min(Y), max(Y )]))}


if __name__ =="__main__":
    app.run_server(debug=True)



# Pega o nome do processador (dependendo do sistema operacional é diferente)
# def get_processor_name():
#     if platform.system() == "Windows":
#         return platform.processor()
#     elif platform.system() == "Linux":
#         command = "cat /proc/cpuinfo"
#         all_info = subprocess.check_output(command, shell=True).decode().strip()
#         for line in all_info.split("\n"):
#             if "model name" in line:
#                 return re.sub( ".*model name.*:", "", line,1)
#     return ""

# def main():
#     # a= 1

      #loop infinito
#     # while a == 1:
#         print(get_processor_name())
#         print(f"Operating system: {platform.system()}")
#         print(f"Current CPU utilization: {psutil.cpu_percent(interval=1)}")
#         #System-wide per-CPU utilization
#         print(f"Current per-CPU utilization: {psutil.cpu_percent(interval=1, percpu=True)}")

#         #Total RAM
#         print(f"Total RAM installed: {round(psutil.virtual_memory().total/1000000000, 2)} GB")
#         #Available RAM
#         print(f"Available RAM: {round(psutil.virtual_memory().available/1000000000, 2)} GB")
#         #Used RAM
#         print(f"Used RAM: {round(psutil.virtual_memory().used/1000000000, 2)} GB")
#         #RAM usage
#         print(f"RAM usage: {psutil.virtual_memory().percent}%")
#         print("   ")
#         subprocess.check_call([r"C:\pathToYourProgram\yourProgram.exe", "your", "arguments", "comma", "separated"])
#         time.sleep(3)

# if __name__ == "__main__":
#     main()