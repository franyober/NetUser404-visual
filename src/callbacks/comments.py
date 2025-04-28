from dash import Input, Output, html, dash_table
import pandas as pd
from api import get_comments

def register_comments_callbacks(app):
    @app.callback(
        Output("comments-table", "children"),
        [Input("sel-date", "date"),
         Input("sel-bssid", "value"),
         Input("sel-MAC", "value")]
    )
    def update_comments_table(selected_date, selected_bssid, selected_mac):
        if not selected_bssid:
            return html.Div("Seleccione un BSSID para ver comentarios.")

        comments = get_comments(selected_date, selected_bssid, selected_mac)
        if not comments:
            return html.Div("No hay comentarios para esta combinación.")

        df = pd.DataFrame(comments)

        table = dash_table.DataTable(
            columns=[{"name": col.capitalize(), "id": col} for col in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'backgroundColor': 'var(--bg-accent)',
                'color': 'var(--text-primary)',
                'textAlign': 'center',
                'padding': '8px',
                'fontSize': '14px',
            },
            style_header={
                'backgroundColor': 'var(--bg-secondary)',
                'fontWeight': 'bold'
            },
            page_size=10
        )

        return table
