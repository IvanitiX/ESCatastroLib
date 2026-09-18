import requests

class MapaValoresUrbanosProvider:
    """Provider para consulta de valores urbanos del Catastro.

    Proporciona métodos para consultar los valores catastrales
    por metro cuadrado de suelo y construcción en zonas urbanas,
    utilizando el mapa de valores del Catastro.

    Attributes:
        URL_BASE: URL base del servicio de mapa de valores urbanos.
    """
    URL_BASE = "https://www1.sedecatastro.gob.es/Cartografia/SECDameGeoJSON.aspx"
    
    def consultar_valores_urbanos_m2(self, x: float, y: float, anio: int, srs: str = "4326") -> requests.Response:
        params = {
            'huso': srs,
            'x':x,
            'y':y,
            'anyoZV':anio,
            'suelo':"N",
            'tipo_mapa':"vivienda"
        }

        peticion = requests.get(self.URL_BASE, params=params, timeout=15)
        peticion.raise_for_status()

        return peticion