from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests

app = Dash()

api_url = 'http://192.168.192.192:8000'
# Peticiones al servidor
def count_status_codes(date):
    PARAMS = {"date": date}
    r = requests.get(f'{api_url}/metrics/errors-count', params=PARAMS)
    count_codes = r.json()
    return count_codes

# Diseño de la página
app.layout = [html.H1('Monitoreo de la red'), 
              dcc.DatePickerSingle(
                  id = "sel-date",
                  date = "2025-02-23"
              ),
              dcc.Graph(id="graph")
             ]



@app.callback(
        Output("graph", "figure"), # figure = graph
        Input("sel-date", "date")  # date = sel-date
)
def update_chart(selected_date):
    # Creando los gráficos
    codes = count_status_codes(selected_date)
    df = pd.DataFrame(codes)
    if df.empty:
        fig = px.pie(title="No hay registros")
    else:
        fig = px.pie(df,values="count",names="status",title=f"Codigos de estado en {selected_date}")
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)

