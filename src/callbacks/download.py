from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd
from assets.fig_layout import my_figlayout
from api import get_download
import plotly.express as px

def register_download_callbacks(app):
    @app.callback(
        Output("linegraph-download", "figure"),
        [Input("sel-date", "date"), 
         Input("sel-bssid", "value"),
         Input("sel-MAC", "value")]
)
    def update_download_chart(selected_date, selected_bssid, selected_mac):
        if not selected_bssid:
            fig = px.line(title="Seleccione un BSSID")
            fig.update_layout(my_figlayout)
            return fig
        
        download = get_download(selected_date, selected_bssid, selected_mac)
        df = pd.DataFrame(download)
        
        if df.empty:
            fig = px.line(title="No hay datos para la combinación selecionada")
            fig.update_layout(my_figlayout)
            return fig
        
        # Procesamiento de fecha
        df["time"] = pd.to_datetime(
            selected_date + " " + df["hour"], 
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        ).dropna()

        # --- Procesamiento de gaps ---
        if not df.empty:
            # Ordenar y calcular diferencias
            df = df.sort_values("time").reset_index(drop=True)
            threshold = pd.Timedelta(minutes=5)
            df["time_diff"] = df["time"].diff()
            
            # Identificar gaps
            gap_indices = df.index[df["time_diff"] > threshold].tolist()
            
            # Mantener solo columnas esenciales
            df = df[["time", "download"]].copy()
            
            # Crear nuevas filas
            new_rows = []
            for idx in gap_indices:
                if idx == 0: continue
                prev_time = df.loc[idx-1, "time"]
                new_time = prev_time + threshold
                new_rows.append({"time": new_time, "download": None})
            
            # Insertar gaps
            if new_rows:
                new_rows_df = pd.DataFrame(new_rows)
                new_rows_df = new_rows_df.astype(df.dtypes)  # Mantener tipos de datos
                df = pd.concat([df, new_rows_df], ignore_index=True)
            
            # Reordenar final
            df = df.sort_values("time").reset_index(drop=True)

        # --- Creación del gráfico ---
        fig = go.Figure()
        
        # Línea principal con gaps
        fig.add_trace(go.Scattergl(
            x=df["time"],
            y=df["download"],
            mode='lines',
            line=dict(color='white', width=1),
            showlegend=False,
            connectgaps=False,
            hovertemplate="<b>Hora:</b> %{x|%H:%M:%S}<br><b>Download:</b> %{y:.2f} s<extra></extra>" 
        ))
        
        # Marcadores transparentes
        fig.add_trace(go.Scattergl(
            x=df["time"],
            y=df["download"],
            mode='markers',
            marker=dict(color='black', size=3, opacity=0),
            visible='legendonly',
            showlegend=False,
            hovertemplate="<b>Hora:</b> %{x|%H:%M:%S}<br><b>Download:</b> %{y:.2f} s<extra></extra>",
            connectgaps=False
        ))

        # Layout personalizado
        fig.update_layout(
            my_figlayout,
            title="Download Time",
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
            yaxis=dict(showspikes=False),
            uirevision='constant'
        )
        
        return fig