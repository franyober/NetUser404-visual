from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime

app = Dash()

api_url = 'http://192.168.192.192:8000'

# Obtener lista de bssid únicos desde la API
def get_bssid_list():
    try:
        r = requests.get(f'{api_url}/metrics/network')
        data = r.json()
        
        if isinstance(data, dict) and "network" in data:
            bssids = data["network"]
            return [{"label": bssid, "value": bssid} for bssid in bssids]
        else:
            return []
    except requests.exceptions.RequestException:
        return []

# Funciones para obtener datos desde la API
def count_status_codes(date, bssid):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/errors-count', params=PARAMS)
        return r.json()
    except:
        return []

def delays_5min(date, bssid):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/delay', params=PARAMS)
        return r.json()
    except:
        return []

hoy = datetime.now().strftime("%Y-%m-%d")

# Layout de la aplicación
app.layout = html.Div([
    html.H1('Monitoreo de la red'),

    dcc.DatePickerSingle(
        id="sel-date",
        date=hoy
    ),

    dcc.Dropdown(
        id="sel-bssid",
        options=[],  # Inicialmente vacío, se llenará dinámicamente
        placeholder="Select a Network",
        style={"width": "50%"}
    ),

    html.Button("Update Network", id="update-bssid-btn", n_clicks=0),

    html.Div([
        html.Div(dcc.Graph(id="piegraph-status"), style={"width": "28%", "display": "inline-block"}),
        html.Div(dcc.Graph(id="linegraph-delay"), style={"width": "68%", "display": "inline-block"})
    ], style={"display": "flex", "justify-content": "space-between"})
])

# Callback para actualizar la lista de BSSID dinámicamente
@app.callback(
    Output("sel-bssid", "options"),
    Input("update-bssid-btn", "n_clicks")
)
def update_bssid_options(n_clicks):
    return get_bssid_list()

# Callback para actualizar el gráfico de códigos de estado
@app.callback(
    Output("piegraph-status", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_pie_chart(selected_date, selected_bssid):
    if not selected_bssid:
        return px.pie(title="Seleccione un BSSID")
    
    codes = count_status_codes(selected_date, selected_bssid)
    df = pd.DataFrame(codes)

    if df.empty:
        return px.pie(title="No hay registros")
    
    return px.pie(df, values="count", names="status", title=f"Códigos de estado en {selected_date} - {selected_bssid}")

# Callback para actualizar el gráfico de latencia
@app.callback(
    Output("linegraph-delay", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_line_chart(selected_date, selected_bssid):
    if not selected_bssid:
        return px.line(title="Seleccione un BSSID")
    
    delays = delays_5min(selected_date, selected_bssid)
    df = pd.DataFrame(delays)

    if df.empty:
        return px.line(title="No hay datos de delay")
    
    df["time"] = pd.to_datetime(df["minute"], format="%H:%M")
    return px.line(df, x="time", y="avg_delay", markers=True, title=f"Latencia promedio cada 5 minutos en {selected_date} - {selected_bssid}")

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
