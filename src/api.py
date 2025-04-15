import requests

api_url = 'http://192.168.192.192:8000'

def get_urls_list():
    try:
        r = requests.get(f'{api_url}/pages')
        data = r.json()
        
        if isinstance(data, dict) and "pages" in data:
            urls = data["pages"]
            return [{"label": url, "value": url} for url in urls]
        else:
            return []
    except requests.exceptions.RequestException:
        return []
    
def get_mac_list():
    try:
        r = requests.get(f'{api_url}/MAC_list')
        data = r.json()
        print(data)
        
        if isinstance(data, dict) and "MAC_list" in data:
            macs = data["MAC_list"]
            return [{"label": mac, "value": mac} for mac in macs]
        else:
            return []
    except requests.exceptions.RequestException:
        return []


def get_bssid_list():
    try:
        r = requests.get(f'{api_url}/networks')
        data = r.json()     
        if isinstance(data, dict) and "network" in data:
            bssids = data["network"]
            return [{"label": bssid, "value": bssid} for bssid in bssids]
        else:
            return []
    except requests.exceptions.RequestException:
        return []
#----------------------------------------------------------------------------------------------
# Funciones para obtener datos desde la API
def count_status_codes(date, bssid, url):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "url": url}
    try:
        r = requests.get(f'{api_url}/metrics/status_code', params=PARAMS)
        return r.json()
    except:
        return []
#---------------------------------------------------------------------------------------------
def get_delays(date, bssid):
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/latency', params=PARAMS)
        data = r.json()
        
        # Debug: Verificar estructura
        
        
        # La API devuelve una lista de diccionarios como muestras
        if isinstance(data, list) and all(isinstance(x, dict) for x in data):
            return data
        else:
            print(f"Estructura inesperada: {type(data)} - {data}")
            return []
            
    except Exception as e:
        print(f"Error en API: {str(e)}")
        return []
#---------------------------------------------------------------------------------------------
def get_load(date, bssid, url):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "url": url}
    try:
        r = requests.get(f'{api_url}/metrics/load', params=PARAMS)
        data = r.json()
        
        # Maneja diferentes estructuras de respuesta
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            if 'detail' in data:  # Si viene un mensaje de error
                print(f"Error en API: {data['detail']}")
                return []
            return [data]  # Convertir a lista para consistencia
        return []
    except Exception as e:
        print(f"Error en get_load: {str(e)}")
        return []
##--------------------------------------------------------------------------------------------
def get_download(date, bssid):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid}
    try:
        r = requests.get(f'{api_url}/metrics/download', params=PARAMS)
        return r.json()
    except:
        return []   