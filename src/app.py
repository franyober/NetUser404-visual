from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, "assets/style.css"])
app.layout = create_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)