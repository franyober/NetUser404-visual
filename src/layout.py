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
                    # Selector de fecha
                    dbc.Col(
                        dcc.DatePickerSingle(
                            id="sel-date",
                            date=hoy,
                            className="dark-datepicker-force",
                            style={
                                "width": "40%",
                                "background-color": "transparent",
                                "color": "white",
                                
                            },
                        ),
                        width=1,
                        style={"padding": "0 5px"}
                    ),
                    
                    # Dropdown BSSID
                    dbc.Col(
                        dcc.Dropdown(
                            id="sel-bssid",
                            options=[],
                            placeholder="Select a Network",
                            style={"width": "90%"}
                        ),
                        width=3,
                        style={"padding": "0 5px"}
                    ),
                    
                    # Dropdown URL
                    dbc.Col(
                        dcc.Dropdown(
                            id="sel-urls",
                            options=[],
                            placeholder="Select a URL",
                            style={"width": "90%"}
                        ),
                        width=4,
                        style={"padding": "0 5px"}
                    ),

                    # Dropdown MAC
                    dbc.Col(
                        dcc.Dropdown(
                            id="sel-MAC",
                            options=[],
                            placeholder="Select a MAC",
                            style={"width": "100%"}
                        ),
                        width=3,
                        style={"padding": "0 5px"}
                    ),
                ],
                className="g-0",  # Elimina espacios entre columnas
                justify="start",  # Alineación a la izquierda
                align="center",
                style={"margin-bottom": "15px", "row-gap": "10px"}
            ),
            
            # Sección de gráficos (igual que tu versión original)
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