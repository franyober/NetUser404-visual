from dash import Input, Output
from api import get_bssid_list, get_urls_list, get_mac_list

def register_dropdown_callbacks(app):
    @app.callback(
        Output("sel-bssid", "options"),
        Input("sel-date", "date")
    )
    def update_bssid_options(selected_date):
        return get_bssid_list()

    @app.callback(
        Output("sel-urls", "options"),
        Input("sel-date", "date") 
    )
    def update_urls_options(selected_date):
        return get_urls_list()

    @app.callback(
        Output("sel-MAC", "options"),
        Input("sel-date", "date") 
    )
    def update_macs_options(selected_date):
        return get_mac_list()