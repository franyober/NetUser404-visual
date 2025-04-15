from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
from assets.fig_layout import my_figlayout

def create_layout():
    hoy = datetime.now().strftime("%Y-%m-%d")
    
    return dbc.Container(
        [
            html.H1("Monitoreo de la red", style={"textAlign": "center", "margin-bottom": "20px"}),
            
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
            
            html.Div(
                [
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
                style={"width": "100%", "margin": "0 auto"}
            ),
        ],
        fluid=True,
        style={"padding": "10px"}
    )