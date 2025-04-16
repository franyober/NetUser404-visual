from dash import Input, Output, State, no_update
from api import get_bssid_list, get_urls_list, get_mac_list

def register_dropdown_callbacks(app):
    # Callback unificado para BSSID (opciones + valor)
    @app.callback(
        Output("sel-bssid", "options"),
        Output("sel-bssid", "value"),
        Input("sel-MAC", "value"),
        Input("sel-date", "date"),
        State("sel-bssid", "value")
    )
    def update_bssid(selected_mac, selected_date, current_bssid):
        try:
            # Obtener nuevas opciones
            new_options = get_bssid_list(mac=selected_mac)
            
            # Verificar si hay opciones válidas
            if not new_options:
                return [], None
            
            # Validar selección actual
            valid_bssids = [opt["value"] for opt in new_options]
            new_value = current_bssid if current_bssid in valid_bssids else None
            
            return new_options, new_value
        
        except Exception as e:
            print(f"Error en callback BSSID: {str(e)}")
            return [], None

    # Callback unificado para MAC (opciones + valor)
    @app.callback(
        Output("sel-MAC", "options"),
        Output("sel-MAC", "value"),
        Input("sel-bssid", "value"),
        Input("sel-date", "date"),
        State("sel-MAC", "value")
    )
    def update_mac(selected_bssid, selected_date, current_mac):
        try:
            new_options = get_mac_list(bssid=selected_bssid)
            
            if not new_options:
                return [], None
            
            valid_macs = [opt["value"] for opt in new_options]
            new_value = current_mac if current_mac in valid_macs else None
            
            return new_options, new_value
        
        except Exception as e:
            print(f"Error en callback MAC: {str(e)}")
            return [], None

    # Callback para URLs
    @app.callback(
        Output("sel-urls", "options"),
        Input("sel-date", "date")
    )
    def update_urls_options(selected_date):
        return get_urls_list()

    # Callback para mantener URL válida
    @app.callback(
        Output("sel-urls", "value"),
        Input("sel-bssid", "value"),
        Input("sel-MAC", "value"),
        State("sel-urls", "value"),
        State("sel-urls", "options")
    )
    def validate_url(selected_bssid, selected_mac, current_url, url_options):
        valid_urls = [opt["value"] for opt in url_options]
        return current_url if current_url in valid_urls else None

    # Eliminar los callbacks de reset que causan conflicto