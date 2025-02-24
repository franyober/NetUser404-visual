from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime

app = Dash()

api_url = 'http://192.168.192.192:8000'
# Peticiones al servidor
def count_status_codes(date):
    PARAMS = {"date": date}
    r = requests.get(f'{api_url}/metrics/errors-count', params=PARAMS)
    count_codes = r.json()
    return count_codes

def delays_5min(date):
    PARAMS = {"date": date}
    r = requests.get(f'{api_url}/metrics/delay', params=PARAMS)
    delays = r.json()
    return delays

hoy = datetime.now().strftime("%Y-%m-%d")

# Diseño de la página
app.layout = html.Div([
    html.H1('Monitoreo de la red'),

    dcc.DatePickerSingle(
        id="sel-date",
        date=hoy
    ),

    # Contenedor para colocar gráficos en dos columnas
    html.Div([
        html.Div(dcc.Graph(id="piegraph-status"), style={"width": "28%", "display": "inline-block"}),
        html.Div(dcc.Graph(id="linegraph-delay"), style={"width": "68%", "display": "inline-block"})
    ], style={"display": "flex", "justify-content": "space-between"})
])

# Actualización del gráfico de la cantidad de códigos de estado
@app.callback(
        Output("piegraph-status", "figure"), # figure = graph
        Input("sel-date", "date")  # date = sel-date
)
def update_pie_chart(selected_date):
    # Creando los gráficos
    codes = count_status_codes(selected_date)
    df = pd.DataFrame(codes)
    if df.empty:
        fig = px.pie(title="No hay registros")
    else:
        fig = px.pie(df,values="count",names="status",title=f"Codigos de estado en {selected_date}")
    
    return fig

# Callback para actualizar el gráfico de delay
@app.callback(
    Output("linegraph-delay", "figure"),
    Input("sel-date", "date")
)
def update_line_chart(selected_date):
    delays = delays_5min(selected_date)
    df = pd.DataFrame(delays)

    if df.empty:
        fig = px.line(title="No hay datos de delay")
    else:
        df["time"] = pd.to_datetime(df["minute"], format="%H:%M")         
        fig = px.line(df, x="time", y="avg_delay", markers=True, title=f"Latencia promedio cada 5 minutos en {selected_date}")
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)

