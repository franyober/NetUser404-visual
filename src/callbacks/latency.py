from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd
from assets.fig_layout import my_figlayout
from api import get_delays
import plotly.express as px

def register_latency_callbacks(app):
    @app.callback(
        Output("linegraph-delay", "figure"),
        [Input("sel-date", "date"), 
         Input("sel-bssid", "value"),
         Input("sel-MAC", "value")]
)
    def update_latency_chart(selected_date, selected_bssid, selected_mac):
        if not selected_bssid:
            fig = go.Figure(layout=my_figlayout)
            fig.update_layout(title="Seleccione un BSSID")
            return fig
            
        delays = get_delays(selected_date, selected_bssid, selected_mac)
        df = pd.DataFrame(delays)
        
        if df.empty:
            fig = px.line(title="No hay datos de delay")
            fig.update_layout(my_figlayout)
            return fig
        
        df["time"] = pd.to_datetime(selected_date + " " + df["hour"], format="%Y-%m-%d %H:%M:%S")
        df = df.sort_values('time').dropna(subset=['time', 'delay'])
        
        x_lines = []
        y_lines = []
        
        for _, row in df.iterrows():
            x_lines.extend([row["time"], row["time"], None])
            y_lines.extend([0, row["delay"], None])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scattergl(
            x=x_lines,
            y=y_lines,
            mode='lines',
            line=dict(color='cyan', width=1),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scattergl(
            x=df["time"],
            y=df["delay"],
            mode='markers',
            marker=dict(size=4, color='black'),
            showlegend=False,
            hoverinfo='x+y'
        ))
        
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