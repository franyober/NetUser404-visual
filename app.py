from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime

app = Dash()

api_url = 'http://192.168.192.192:8000'
#------------------------------------------------------------------------------------------------
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
#----------------------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------------------
def delays_5min(date, bssid):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/delay', params=PARAMS)
        return r.json()
    except:
        return []
#---------------------------------------------------------------------------------------------
def load_5min(date, bssid):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/loadtime', params=PARAMS)
        return r.json()
    except:
        return []
##--------------------------------------------------------------------------------------------
def download_5min(date, bssid):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/download', params=PARAMS)
        return r.json()
    except:
        return []   
##--------------------------------------------------------------------------------------------
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
        html.Div(dcc.Graph(id="piegraph-status"), style={"width": "30%", "display": "inline-block"}),
        html.Div([
            dcc.Graph(id="linegraph-delay",    style={"width": "100%"}),
            dcc.Graph(id="linegraph-load",     style={"width": "100%"}),
            dcc.Graph(id="linegraph-download", style={"width": "100%"})
            
        ], style={"width": "68%", "display": "inline-block", "vertical-align": "top"})
    ], style={"display": "flex", "justify-content": "space-between", "width": "100%"})
])


# Callback para actualizar la lista de BSSID dinámicamente----------------------------------
@app.callback(
    Output("sel-bssid", "options"),
    Input("update-bssid-btn", "n_clicks")
)
def update_bssid_options(n_clicks):
    return get_bssid_list()

# Callback para actualizar el gráfico de códigos de estado-----------------------------------
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

# Callback para actualizar el gráfico de latencia (Needle Plot)--------------------------------------------------------
@app.callback(
    Output("linegraph-delay", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_latency_chart(selected_date, selected_bssid):
    if not selected_bssid:
        return go.Figure(layout_title_text="Seleccione un BSSID")
    
    delays = delays_5min(selected_date, selected_bssid)
    df = pd.DataFrame(delays)
    
    if df.empty:
        return go.Figure(layout_title_text="No hay datos de delay")
    
    df["time"] = pd.to_datetime(selected_date + " " + df["minute"], format="%Y-%m-%d %H:%M")

    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["time"], 
        y=df["avg_delay"], 
        mode='markers', 
        marker=dict(size=8, color='blue'),
        name="Latencia"
    ))
    
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["time"], row["time"]],
            y=[0, row["avg_delay"]],
            mode='lines',
            line=dict(color='blue', width=2),
            showlegend=False
        ))
    
    fig.update_layout(
        title=f"Latencia promedio cada 5 minutos en {selected_date} - {selected_bssid}",
        xaxis_title="Hora",
        yaxis_title="Latencia (ms)",
        showlegend=True
    )
    
    return fig

# Callback para actualizar el gráfico de tiempo de carga de páginas (Needle Plot)----------------------------------------------------
@app.callback(
    Output("linegraph-load", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_load_chart(selected_date, selected_bssid):
    if not selected_bssid:
        return go.Figure(layout_title_text="Seleccione un BSSID")
    
    loads = load_5min(selected_date, selected_bssid)
    df = pd.DataFrame(loads)
    
    if df.empty:
        return go.Figure(layout_title_text="No hay datos de load")
    
    df["time"] = pd.to_datetime(selected_date + " " + df["minute"], format="%Y-%m-%d %H:%M")

    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["time"], 
        y=df["avg_load"], 
        mode='markers', 
        marker=dict(size=8, color='orange'),
        name="Tiempo de carga"
    ))
    
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["time"], row["time"]],
            y=[0, row["avg_load"]],
            mode='lines',
            line=dict(color='orange', width=2),
            showlegend=False
        ))
    
    fig.update_layout(
        title=f"Tiempo de carga promedio cada 5 minutos en {selected_date} - {selected_bssid}",
        xaxis_title="Hora",
        yaxis_title="Load time (ms)",
        showlegend=True
    )
    
    return fig

# Callback para actualizar el gráfico de tiempo de carga de páginas (Needle Plot)-------------------------
@app.callback(
    Output("linegraph-download", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_download_chart(selected_date, selected_bssid):
    if not selected_bssid:
        return px.line(title="Seleccione un BSSID")
    
    download = download_5min(selected_date, selected_bssid)
    df = pd.DataFrame(download)

    if df.empty:
        return px.line(title="No hay datos de download")
    
    df["time"] = pd.to_datetime(selected_date + " " + df["minute"], format="%Y-%m-%d %H:%M")
    return px.line(df, x="time", y="avg_download", markers=True, title=f"Velocidad de descarga cada 5 minutos en {selected_date} - {selected_bssid}")


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
