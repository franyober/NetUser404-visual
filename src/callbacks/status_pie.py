from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from assets.fig_layout import my_figlayout
from api import count_status_codes

def register_status_callbacks(app):
    @app.callback(
        Output("piegraph-status", "figure"),
        [Input("sel-date", "date"), Input("sel-bssid", "value"), Input("sel-urls", "value")]
    )
    def update_pie_chart(selected_date, selected_bssid, selected_url):
        if not selected_bssid:
            return go.Figure().update_layout(my_figlayout)
        
        try:
            if not selected_url:
                return go.Figure().update_layout(my_figlayout)
                
            codes = count_status_codes(selected_date, selected_bssid, selected_url)
            
            if isinstance(codes, dict) and 'detail' in codes:
                return go.Figure().update_layout(my_figlayout)
                
            if not codes:
                return go.Figure().update_layout(my_figlayout)
                
            df = pd.DataFrame(codes)
            fig = px.pie(df, values="count", names="status", title="Códigos de estado")
            return fig.update_layout(my_figlayout)
            
        except Exception as e:
            return go.Figure().update_layout(my_figlayout)