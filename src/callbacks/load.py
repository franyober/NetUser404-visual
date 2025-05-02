from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd
from assets.fig_layout import my_figlayout
from api import get_load

def register_load_callbacks(app):
    @app.callback(
    Output("linegraph-load", "figure"),
    [Input("sel-date", "date"), 
     Input("sel-bssid", "value"), 
     Input("sel-urls", "value"), 
     Input("sel-MAC", "value")]
    )
    def update_load_chart(selected_date, selected_bssid, selected_url, selected_mac):
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
            loads = get_load(selected_date, selected_bssid, selected_url, selected_mac)
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
            # --- Nuevo: Procesamiento de gaps ---
            # Ordenar por tiempo
            df = df.sort_values('time').reset_index(drop=True)

            # Umbral para considerar un gap (5 minutos)
            threshold = pd.Timedelta(minutes=5)

            # Calcular diferencias de tiempo
            df['time_diff'] = df['time'].diff()

            # Identificar gaps mayores al umbral
            gap_indices = df.index[df['time_diff'] > threshold].tolist()

            # Mantener solo columnas esenciales (excluyendo 'hour' y otras)
            df = df[["time", "load"]].copy()  # <--- ¡Clave! Eliminar columnas no usadas

            # Crear nuevas filas con estructura idéntica
            new_rows = []
            for idx in gap_indices:
                if idx == 0:
                    continue
                prev_time = df.loc[idx - 1, 'time']
                new_time = prev_time + threshold
                new_rows.append({'time': new_time, 'load': None})

            # Insertar nuevos registros (sin columnas adicionales)
            if new_rows:
                new_rows_df = pd.DataFrame(new_rows)
                # Asegurar mismas columnas y tipos
                new_rows_df = new_rows_df.astype(df.dtypes)  # <--- ¡Corrección final!
                df = pd.concat([df, new_rows_df], ignore_index=True)

            # Re-ordenar y asegurar tipos
            df = df.sort_values('time').reset_index(drop=True)
            # --- Fin de procesamiento de gaps ---
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
                hovertemplate="<b>Hora:</b> %{x|%H:%M:%S}<br><b>Load:</b> %{y:.2f} s<extra></extra>",
                connectgaps=False
            ))
            
            # 6. Configuración final (SIN líneas blancas)
            fig.update_layout(
            my_figlayout,
            title="Tiempo de carga de páginas",
            xaxis_title="Hora",
            yaxis_title="Tiempo (s)",
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

