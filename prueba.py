from dash import Dash, html, dcc
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



# Creando los gráficos
codes = count_status_codes("2025-02-23")
df = pd.DataFrame(codes)
fig = px.pie(df,values="count",names="status")


# Diseño de la página
app.layout = [html.H1('Monitoreo de la red'), 
              dcc.Graph(figure=fig)
             ]


if __name__ == '__main__':
    app.run(debug=True)

