# NetUser404 - Visual

Este módulo forma parte del sistema **NetUser404** y está diseñado para visualizar métricas de conectividad a internet recolectadas por las estaciones cliente. Utiliza **Dash** y **Plotly** para ofrecer una interfaz interactiva con filtros y gráficos en tiempo real.

## Características

- Filtros interactivos por:
  - Fecha
  - Red (BSSID)
  - MAC Address
  - URL accedida
- Visualización de:
  - Códigos de estado HTTP (gráfico de torta)
  - Tiempo de carga de páginas (gráfico lineal)
  - Latencia (gráfico de líneas verticales)
  - Velocidad de descarga (gráfico lineal)

---

## Requisitos

* Solo disponible para Linux
* Python 3.10 o superior
* Conectividad con la API de [NetUser404-api](https://github.com/franyober/NetUser404-api)


## Instalación

En la terminal, ejecutar el siguiente comando para descargar el instalador:
```
wget https://raw.githubusercontent.com/franyober/NetUser404-visual/refs/heads/main/install_visual
```

Luego, dar permisos de ejecución a `install_visual`:
```
sudo chmod +x install_visual
```

Luego, ejecutar el instalador:
```
sudo ./install_visual
```

### Desinstalación

Para desinstalar, se recomienda descargar el siguiente script de desinstalación:

```
wget https://raw.githubusercontent.com/franyober/NetUser404-visual/refs/heads/main/uninstall_visual
```

Los pasos para ejecutar el script de desinstalación son los mismos que se usó para el de instalación.


