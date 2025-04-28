import requests

api_url = 'http://127.0.0.1:80'

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
    
def get_mac_list(bssid=None, date=None):
    try:
        PARAMS = {}
        endpoint = '/MAC_list'  # Por defecto
        
        if bssid:
            endpoint = '/macs_by_bssid'
            PARAMS["bssid"] = bssid
        
        if date:
            PARAMS["date"] = date  # Siempre enviar fecha
        
        r = requests.get(f'{api_url}{endpoint}', params=PARAMS)
        data = r.json()
        
        return [{"label": mac, "value": mac} for mac in data.get("MAC_list", [])]
        
    except Exception as e:
        print(f"Error en get_mac_list: {str(e)}")
        return []

def get_bssid_list(mac=None):
    try:
        PARAMS = {"mac": mac} if mac else {}
        endpoint = '/bssids_by_mac' if mac else '/networks'
        r = requests.get(f'{api_url}{endpoint}', params=PARAMS)
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
def count_status_codes(date, bssid, url, mac=None):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "url": url}
    if mac is not None:  # Solo agregar mac si tiene valor
        PARAMS["mac"] = mac
    
    try:
        r = requests.get(f'{api_url}/metrics/status_code', params=PARAMS)
        return r.json()
    except:
        return []
#---------------------------------------------------------------------------------------------
def get_delays(date, bssid, mac=None):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "mac": mac}
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
def get_load(date, bssid, url, mac = None):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "url": url, "mac": mac}
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
def get_download(date, bssid, mac = None):
    if not bssid:
        return []
    
    PARAMS = {"date": date, "bssid": bssid, "mac": mac}
    try:
        r = requests.get(f'{api_url}/metrics/download', params=PARAMS)
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
##--------------------------------------------------------------------------------------------
def get_comments(date, bssid, mac=None):
    try:
        params = {"date": date, "bssid": bssid}
        if mac:
            params["mac"] = mac

        r = requests.get(f"{api_url}/metrics/comments", params=params)
        return r.json()  # Esperamos lista de diccionarios
    except Exception as e:
        print(f"Error en get_comments: {str(e)}")
        return []
