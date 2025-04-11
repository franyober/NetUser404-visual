from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime




app = Dash(__name__, external_stylesheets=["assets/style.css"])
from assets.fig_layout import my_figlayout


api_url = 'http://127.0.0.1:8000'
#------------------------------------------------------------------------------------------------
# Obtener lista de bssid únicos desde la API

def get_urls_list():
    try:
        r = requests.get(f'{api_url}/pages')
        data = r.json()
        
        if isinstance(data, dict) and "pages" in data:
            urls = data["pages"]
            return [{"label": url, "value": url} for url in urls]
        else:
            return []
    except requests.exceptions.RequestException:
        return []
    
def get_mac_list():
    try:
        r = requests.get(f'{api_url}/MAC_list')
        data = r.json()
        print(data)
        
        if isinstance(data, dict) and "MAC_list" in data:
            macs = data["MAC_list"]
            return [{"label": mac, "value": mac} for mac in macs]
        else:
            return []
    except requests.exceptions.RequestException:
        return []


def get_bssid_list():
    try:
        r = requests.get(f'{api_url}/networks')
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
def count_status_codes(date, bssid, url):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "url": url}
    try:
        r = requests.get(f'{api_url}/metrics/status_code', params=PARAMS)
        return r.json()
    except:
        return []
#---------------------------------------------------------------------------------------------
def get_delays(date, bssid):
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/latency', params=PARAMS)
        data = r.json()
        
        # Debug: Verificar estructura
        
        
        # La API devuelve una lista de diccionarios como muestras
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            return data
        else:
            print(f"Estructura inesperada: {type(data)} - {data}")
            return []
            
    except Exception as e:
        print(f"Error en API: {str(e)}")
        return []
#---------------------------------------------------------------------------------------------
def get_load(date, bssid, url):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "url": url}
    try:
        r = requests.get(f'{api_url}/metrics/load', params=PARAMS)
        data = r.json()
        
        # Maneja diferentes estructuras de respuesta
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            if 'detail' in data:  # Si viene un mensaje de error
                print(f"Error en API: {data['detail']}")
                return []
            return [data]  # Convertir a lista para consistencia
        return []
    except Exception as e:
        print(f"Error en get_load: {str(e)}")
        return []
##--------------------------------------------------------------------------------------------
def get_download(date, bssid):
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
app.layout = dbc.Container(
    [
        # Título
        html.H1("Monitoreo de la red", style={"textAlign": "center", "margin-bottom": "20px"}),
        
        # Controles (fecha, BSSID, URL)
        dbc.Row(
            [
                dbc.Col(dcc.DatePickerSingle(
                    id="sel-date",
                    date=hoy,
                    className="dark-datepicker-force",
                    style={"background-color": "transparent", "color": "white", "border": "1px solid #444"},
                ), width=2),
                
                dbc.Col(dcc.Dropdown(
                    id="sel-bssid",
                    options=[],
                    placeholder="Select a Network",
                    style = {"width": "50%"}
                ), width=3),
                
                
                
                dbc.Col(dcc.Dropdown(
                    id="sel-urls",
                    options=[],
                    placeholder="Select a URL",
                    style = {"width": "50%"}
                ), width=3),


                dbc.Col(dcc.Dropdown(
                    id="sel-MAC",
                    options=[],
                    placeholder="Select a MAC",
                    style = {"width": "50%"}
                ), width=3),
                
                
            ],
            className="mb-4",
            justify="between",
        ),
        
        # Grid 2x2 de gráficas (sin espacios)
        html.Div(
            [
                # Fila 1
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(id="piegraph-status"),
                            style={"width": "49%", "display": "inline-block", "margin-right": "1%", "height": "400px"}
                        ),
                        html.Div(
                            dcc.Graph(id="linegraph-load"),
                            style={"width": "49%", "display": "inline-block", "margin-left": "1%", "height": "400px"}
                        ),
                    ],
                    style={"margin-bottom": "10px"}
                ),
                # Fila 2
                html.Div(
                    [
                        html.Div(
                            dcc.Graph(id="linegraph-delay"),
                            style={"width": "49%", "display": "inline-block", "margin-right": "1%", "height": "400px"}
                        ),
                        html.Div(
                            dcc.Graph(id="linegraph-download"),
                            style={"width": "49%", "display": "inline-block", "margin-left": "1%", "height": "400px"}
                        ),
                    ]
                ),
            ],
            style={"width": "100%", "margin": "0 auto"}  # Contenedor principal sin padding
        ),
    ],
    fluid=True,
    style={"padding": "10px"}  # Padding general del contenedor
)

# BSSID dinámicamente---------------------------------------------------------------------------------
@app.callback(
    Output("sel-bssid", "options"),
    Input("sel-date", "date")
)
def update_bssid_options(selected_date):
    return get_bssid_list()

# URLs dinámicamente---------------------------------------------------------------------------------
@app.callback(
    Output("sel-urls", "options"),
    Input("sel-date", "date") 
)
def update_urls_options(selected_date):
    return get_urls_list()
# MAC dinámicamenrte ---------------------------------------------------------------------------------

@app.callback(
    Output("sel-MAC", "options"),
    Input("sel-date", "date") 
)
def update_macs_options(selected_date):
    return get_mac_list()


# SC---------------------------------------------------------------------------------------------------

@app.callback(
    Output("piegraph-status", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value"), Input("sel-urls", "value")]
)
def update_pie_chart(selected_date, selected_bssid, selected_url):
    if not selected_bssid:
        return go.Figure().update_layout(my_figlayout)
    
    try:
        # Verificar parámetro faltante antes de llamar a la API
        if not selected_url:
            return go.Figure().update_layout(my_figlayout)
            
        codes = count_status_codes(selected_date, selected_bssid, selected_url)
        
        if isinstance(codes, dict) and 'detail' in codes:
            # Error de API, pero no lo imprimimos para evitar logs confusos
            return go.Figure().update_layout(my_figlayout)
            
        if not codes:
            return go.Figure().update_layout(my_figlayout)
            
        df = pd.DataFrame(codes)
        fig = px.pie(df, values="count", names="status", title="Códigos de estado")
        return fig.update_layout(my_figlayout)
        
    except Exception as e:
        return go.Figure().update_layout(my_figlayout)

# LATENCY---------------------------------------------------------------------------------------
@app.callback(
    Output("linegraph-delay", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_latency_chart(selected_date, selected_bssid):
    if not selected_bssid:
        fig = go.Figure(layout=my_figlayout)
        fig.update_layout(title="Seleccione un BSSID")
        return fig
        
    delays = get_delays(selected_date, selected_bssid)
    df = pd.DataFrame(delays)
    
    if df.empty:
        fig = px.line(title="No hay datos de delay")
        fig.update_layout(my_figlayout)
        return fig
    
    # Procesamiento eficiente de fechas
    df["time"] = pd.to_datetime(selected_date + " " + df["hour"], format="%Y-%m-%d %H:%M:%S")
    df = df.sort_values('time').dropna(subset=['time', 'delay'])
    
    # --- Optimización clave: Generar todas las líneas en un solo trace ---
    # Crear arrays para todas las líneas verticales
    x_lines = []
    y_lines = []
    
    for _, row in df.iterrows():
        x_lines.extend([row["time"], row["time"], None])  # None separa las líneas
        y_lines.extend([0, row["delay"], None])
    
    fig = go.Figure()
    
    # 1. Trace único para todas las líneas verticales
    fig.add_trace(go.Scattergl(
        x=x_lines,
        y=y_lines,
        mode='lines',
        line=dict(color='cyan', width=1),
        showlegend=False,
        hoverinfo='skip'  # Desactiva hover para líneas
    ))
    
    # 2. Trace para los puntos (usando Scattergl para acelerar)
    fig.add_trace(go.Scattergl(
        x=df["time"],
        y=df["delay"],
        mode='markers',
        marker=dict(size=4, color='black'),
        showlegend=False,
        hoverinfo='x+y'  # Mostrar info solo en puntos
    ))
    
    # Layout (igual que antes)
    fig.update_layout(
        my_figlayout,
        title="Latency (Optimized)",
        xaxis_title="Hora",
        yaxis_title="Tiempo (ms)",
        hovermode="x unified",
        xaxis=dict(
            type='date',
            rangeslider=dict(visible=True, thickness=0.08),
            range=[df["time"].min(), df["time"].min() + pd.Timedelta(minutes=30)],
            tickformat="%H:%M",
            dtick=1800000,
            showspikes=False
        ),
        yaxis=dict(showspikes=False)
    )
    
    return fig

# LOADTIME---------------------------------------------------------------------------------------------------
@app.callback(
    Output("linegraph-load", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value"), Input("sel-urls", "value")]
)
def update_load_chart(selected_date, selected_bssid, selected_url):
    if not selected_bssid or not selected_url:
        fig = go.Figure()
        fig.update_layout(
            my_figlayout,
            title="Seleccione un BSSID y una URL" if not selected_bssid else "Seleccione una URL",
            xaxis={"visible": False},
            yaxis={"visible": False}
        )
        return fig
    
    try:
        # 1. Obtener datos
        loads = get_load(selected_date, selected_bssid, selected_url)
        # 2. Verificar y convertir a DataFrame
        if not loads:
            raise ValueError("No se recibieron datos de carga")
            
        df = pd.DataFrame(loads)
        
        # 3. Verificar columnas requeridas
        required_columns = {'hour', 'load'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Columnas faltantes: {missing}. Columnas disponibles: {df.columns.tolist()}")
        
        # 4. Procesamiento de fechas
        df["time"] = pd.to_datetime(
            selected_date + " " + df["hour"],
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        ).dropna()
        
        if df.empty:
            raise ValueError("No hay datos válidos después de procesamiento")
        
        # 5. Crear gráfico
        fig = go.Figure()
        
        # Línea principal
        fig.add_trace(go.Scattergl(
            x=df["time"],
            y=df["load"],
            mode='lines+markers',
            line=dict(color='#00cc96', width=2),
            marker=dict(size=4, color='#0068c9'),
            name="Tiempo de carga (s)",
            hovertemplate="<b>Hora:</b> %{x|%H:%M:%S}<br><b>Load:</b> %{y:.2f} s<extra></extra>"
        ))
        
        # 6. Configuración final (SIN líneas blancas)
        fig.update_layout(
        my_figlayout,
        title="Load Time",
        xaxis_title="Hora",
        yaxis_title="Tiempo (ms)",
        hovermode="x unified",
        
        # Nuevas configuraciones para el eje X
        xaxis=dict(
            type='date',
            rangeslider=dict(visible=True,
                             thickness=0.08                                     
                             ),  # Barra deslizante para navegar en el tiempo
            range=[df["time"].min(), df["time"].min() + pd.Timedelta(minutes=30)],  # Rango inicial de 30 min
            # Formato de las etiquetas
            tickformat="%H:%M",
            # Frecuencia de las marcas
            dtick=1800000,  # 30 minutos en milisegundos
            showspikes=False,
            spikethickness=0
        ),
        yaxis=dict(
            showspikes=False
        )
    )
    
        return fig
        
    except Exception as e:
        print(f"Error en gráfico de carga: {str(e)}")
        error_fig = go.Figure()
        error_fig.add_annotation(
            text=f"Error: {str(e)}",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return error_fig.update_layout(my_figlayout)
# DOWNLOAD---------------------------------------------------------------------------------------------
@app.callback(
    Output("linegraph-download", "figure"),
    [Input("sel-date", "date"), Input("sel-bssid", "value")]
)
def update_download_chart(selected_date, selected_bssid):
    if not selected_bssid:
        fig = px.line(title="Seleccione un BSSID")
        fig.update_layout(my_figlayout)
        return fig
    
    download = get_download(selected_date, selected_bssid)
    df = pd.DataFrame(download)
    if df.empty:
        fig = px.line(title="No hay datos")
        fig.update_layout(my_figlayout)
        return fig
    
    df["time"] = pd.to_datetime(selected_date + " " + df["hour"], format="%Y-%m-%d %H:%M:%S")

    
    # Crear la figura
    fig = go.Figure()
    
    # Configuración especial para datasets completos
    fig.add_trace(go.Scattergl(
        x=df["time"],
        y=df["download"],
        mode='lines',
        line=dict(color='white', width=1),
        showlegend=False,
        connectgaps=False,  # muestra los huecos como discontinuidades
        hovertemplate="<b>Hora:</b> %{x|%H:%M:%S}<br><b>Download:</b> %{y:.2f} s<extra></extra>" 
    ))
    
    # Marcadores solo visibles al hacer hover/zoom
    fig.add_trace(go.Scattergl(
        x=df["time"],
        y=df["download"],
        mode='markers',
        marker=dict(
            color='black',
            size=3,
            opacity=0  # Invisibles por defecto
        ),
        visible='legendonly',  # Solo aparecen al interactuar
        showlegend=False,
        hovertemplate="<b>Hora:</b> %{x|%H:%M:%S}<br><b>Download:</b> %{y:.2f} s<extra></extra>" 
    ))

    # Aplicar layout personalizado
    fig.update_layout(
            my_figlayout,
            uirevision='constant',
            hoverdistance=10, # Sensibilidad del hover
            title="Download Time",
            xaxis_title="Hora",
            yaxis_title="Tiempo (ms)",
            hovermode="x unified",

            xaxis=dict(
            type='date',
            rangeslider=dict(visible=True,
                             thickness=0.08
                             ),  # Barra deslizante para navegar en el tiempo
            range=[df["time"].min(), df["time"].min() + pd.Timedelta(minutes=30)],  # Rango inicial de 30 min
            # Formato de las etiquetas
            tickformat="%H:%M",
            # Frecuencia de las marcas
            dtick=1800000,  # 30 minutos en milisegundos
            showspikes=False,
            spikethickness=0
                     ),
            yaxis=dict(
            showspikes=False   
                     )
        )
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
