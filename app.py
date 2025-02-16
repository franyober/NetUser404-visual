# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import requests

#API
ip="192.168.192.94"
port="8000"
URL = f"http://{ip}:{port}"

def update_status_codes_count(date):
    PARAMS =  {"date": date} 
    r = requests.get(f"{URL}/metrics/errors-count", params=PARAMS)
    data_json = r.json()
    return data_json

# create the app
app = Dash()

# Iniciar la variable df con la fecha deseada
df = update_status_codes_count("2025-02-16")
df_g = pd.DataFrame(df)

# Crear el gráfico de pastel
fig = px.pie(
    df_g, 
    values="count", 
    names="status", 
    title="Distribución de Códigos HTTP"
)

# App layout
app.layout = html.Div([
    dcc.Interval(
        id='interval',
        disabled=False,
        n_intervals=0,
        interval=1000*10, # cada 10 seg 
        max_intervals=100,
    ),
    html.Div([
        html.Div(id="status", children="Esperando datos...")
    ]),
    dash_table.DataTable(id="status-table", data=df, page_size=10),
    dcc.Graph(id="status-graph", figure=fig)
])

# Callback para actualizar el estado y los gráficos
@app.callback(
    [Output("status", "children"),
     Output("status-table", "data"),
     Output("status-graph", "figure")],
    [Input("interval", "n_intervals")]
)
def update_status_codes_count_div(n):
    # Actualizar la fecha según lo que desees
    date = "2025-02-16"
    
    # Obtener nuevos datos
    data_json = update_status_codes_count(date)
    df_g = pd.DataFrame(data_json)
    
    # Actualizar tabla y gráfico
    fig = px.pie(
        df_g, 
        values="count", 
        names="status", 
        title="Distribución de Códigos HTTP"
    )
    
    # Devolver los nuevos valores para la visualización
    return f"Datos actualizados en: {date}", df_g.to_dict('records'), fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

